import argparse
import logging
import sys
from shutil import rmtree
from os.path import join, isdir
from .fetch_input import fetch_input
from .ingest_ngs import ingest
from .upload_results import upload_results


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)

logger = logging.getLogger("ingest_wrapper")

def main():
    parser = argparse.ArgumentParser(
        description="Fetch source data, chunk it up, and send it to Swift")

    fetch_parser = parser.add_argument_group('Fetch input data')
    fetch_parser.add_argument('--source', '-s', required=True,
                              help='The source url in http')
    fetch_parser.add_argument('--download-dir', '-d', required=True,
                              help="Destination directory")
    fetch_parser.add_argument('--stacks', action='store_true',
                              help='Whether the input is a stack')
    fetch_parser.add_argument('--filter',
                              help="Filename filter regex for container stacks")

    ingest_parser = parser.add_argument_group('Chunk up source data')
    ingest_parser.add_argument('--parameters',
                               help='The ingestion parameters as JSON string')
    ingest_parser.add_argument('--results-dir', '-r', required=True,
                               help="Directory to store results")

    upload_parser = parser.add_argument_group('Upload processed data')
    upload_parser.add_argument('--container', required=True,
                               help="The destination container")
    upload_parser.add_argument('--cleanup',  action='store_true',
                               help="Wipe the local data after a successful upload")
    upload_parser.add_argument('--noupload', action='store_true',
                               help='Use this switch to skip uploading in the end')

    args = parser.parse_args()
    print(args)

    try:
        return_code = 0
        fetch_input(
            source=args.source,
            destination=args.download_dir,
            stacks=args.stacks,
            filter=args.filter)

        if not args.stacks:
            #single file
            ingest_input_path = join(args.download_dir, args.source.split('/')[-1])
        else:
            ingest_input_path = args.download_dir

        ingest(
            path=ingest_input_path,
            destination=args.results_dir,
            parameters=args.parameters)

        if not args.noupload:
            upload_results(
                results_folder=args.results_dir,
                destination_container=args.container)
    except Exception as exc:
        logging.exception(exc)
        logging.error("Ingestion failed")
        return_code = 1
    finally:
        if args.cleanup:
            if isdir(args.download_dir):
                logger.info("Deleting download folder")
                rmtree(args.download_dir)
                logger.info("Done")
            if isdir(args.results_dir):
                logger.info("Deleting results folder")
                rmtree(args.results_dir)
                logger.info("Done")
        sys.exit(return_code)


if __name__ == '__main__':
    main()

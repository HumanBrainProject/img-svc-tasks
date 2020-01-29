import argparse
from os import getcwd
from .fetch_input import fetch_input
from .ingest_ngs import ingest
from .upload_results import upload_results



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
    ingest_parser.add_argument('--parameters', required=True,
                               help='The ingestion parameters as JSON string')
    ingest_parser.add_argument('--results-dir', '-r', required=True,
                               help="Directory to store results")

    upload_parser = parser.add_argument_group('Upload processed data')
    upload_parser.add_argument('--container', required=True,
                               help="The destination container")
    upload_parser.add_argument('--cleanup',  action='store_true',
                               help="Wipe the local data after a successful upload")

    args = parser.parse_args()
    print(args)
    fetch_input(
        source=args.source,
        destination=args.download_dir,
        stacks=args.stacks,
        filter=args.filter)

    ingest(
        path=args.download_dir,
        destination=args.results_dir,
        parameters=args.parameters)

    upload_results(
        results_folder=args.results_dir,
        destination_container=args.container,
        cleanup=args.cleanup)

if __name__ == '__main__':
    main()

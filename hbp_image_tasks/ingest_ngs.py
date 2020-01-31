import sys
import json
import argparse
import logging
from os import getcwd, makedirs
from os.path import isdir, join
from pathlib import Path
from pprint import pformat
from time import perf_counter
from datetime import timedelta



import neuroglancer_scripts.volume_reader
import neuroglancer_scripts.dyadic_pyramid
from neuroglancer_scripts.scripts.compute_scales import compute_scales
from neuroglancer_scripts.scripts.generate_scales_info import generate_scales_info
from neuroglancer_scripts.scripts.slices_to_precomputed import convert_slices_in_directory



logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)

logger = logging.getLogger("ingest")

def __persist_info(path, info):
    with open(join(path, 'info_fullres.json'), 'w') as jfile:
        json.dump(info, jfile)

def ingest(path, destination, parameters_file=None, parameters=None):
    '''
    Arguments
        path (str):
            The location of the input, can be a file or a directory for stacks
        destination(str):
            The path where the results will be written
        parameters_file(str):
            The path of the json file with the ingestion parameters
        parameters(str):
            The ingestion parameters as a string
    '''
    if not isdir(destination):
        makedirs(destination, 0o700)
    if not (parameters_file or parameters):
        sys.exit("No ingestion parameters provided")
    if parameters_file:
        try:
            with open(parameters_file) as df:
                parameters = json.load(df)
        except Exception:
            sys.exit("Couldn't load definition file")
    else:
        parameters = json.loads(parameters)
    ingest_path(path, destination, parameters)

def ingest_path(path, datadir, parameters):
    start = perf_counter()
    logger.info(f'Ingesting with parameters: {pformat(parameters)}')
    if isdir(path) and not parameters:
        raise AttributeError("Info.json required with stack of images")
    if isdir(path) and parameters:
        logger.info("Detected stacks, beginning chunking.")
        __persist_info(datadir, parameters)  # parameters has to be the info
        generate_scales_info(
            input_fullres_info_filename = join(datadir, "info_fullres.json"),
            dest_url=datadir)
        convert_slices_in_directory(
            slice_dirs=[Path(path)],
            dest_url=datadir,
            input_orientation="RAS")
    else:
        # This is a single file, proceed to normal ingestion
        # Generate info
        logger.info("Detected single volume file, beginning chunking.")
        neuroglancer_scripts.volume_reader.volume_file_to_info(
            volume_filename=path,
            dest_url=datadir,
            ignore_scaling=False,
            input_min=None,
            input_max=None,
            options={})
        if parameters.get('data_type'):
            __override_info(
                join(datadir, "info_fullres.json"),
                'data_type',
                parameters.get('data_type'))

        # Generate scales info
        generate_scales_info(
            input_fullres_info_filename = join(datadir, "info_fullres.json"),
            dest_url=datadir)

        # Generate chunks
        neuroglancer_scripts.volume_reader.volume_file_to_precomputed(
            path,
            datadir)
    logger.info("Chunking complete, beginning generating scales.")
    # Compute scales after chunks are there
    compute_scales(
        work_dir=datadir,
        downscaling_method="average",
        options={})
    finish = perf_counter()
    logger.info("Scaling complete.")
    logger.info(f"Finished ingestion in {timedelta(seconds=finish-start)}")

def __override_info(jsonfile, key, value):
    '''Needed for the JuBrain example that gets a faulty data type'''
    with open(jsonfile, 'r') as infile:
        info = json.load(infile)
    info["data_type"] = "uint8"
    with open(jsonfile, 'w') as outfile:
        json.dump(info, outfile)

def main():
    parser = argparse.ArgumentParser(description='Launch ingestions')
    parser.add_argument('source', help='The filesystem path to the source data')
    parser.add_argument('--definition-file', help='The filesystem path to the json '
                        'definition to drive the ingestion')
    parser.add_argument('--definition', help='The definition JSON as string')
    parser.add_argument('--destination', required=True, help="Destination directory")
    arguments = parser.parse_args()

    ingest(
        path=arguments.source,
        destination=arguments.destination,
        parameters_file=arguments.definition_file,
        parameters=arguments.definition)


if __name__ == "__main__":
    main()

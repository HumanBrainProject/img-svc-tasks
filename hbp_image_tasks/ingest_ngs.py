import sys
import json
import argparse
import logging
from os import getcwd, makedirs
from os.path import isdir, join
from pathlib import Path
from pprint import pformat


import neuroglancer_scripts.volume_reader
import neuroglancer_scripts.dyadic_pyramid
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
    logger.info(f'Ingesting with parameters: {pformat(parameters)}')
    ingest_path(path, destination, parameters)

def ingest_path(path, datadir, parameters):

    if isdir(path) and not parameters:
        raise AttributeError("Info.json required with stack of images")
    if isdir(path) and parameters:
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

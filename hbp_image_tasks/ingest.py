import sys
import json
import argparse
from os import getcwd, makedirs
from os.path import isdir, join
from pathlib import Path


import neuroglancer_scripts.volume_reader
import neuroglancer_scripts.dyadic_pyramid
from neuroglancer_scripts.scripts.generate_scales_info import generate_scales_info
from neuroglancer_scripts.scripts.slices_to_precomputed import convert_slices_in_directory

parser = argparse.ArgumentParser(description='Launch ingestions')
parser.add_argument('source', help='The filesystem path to the source data')
parser.add_argument('definition', help='The filesystem path to the json '
                    'definition to drive the ingestion')
parser.add_argument('--destination', default='./results', help="Destination directory")

def __persist_info(path, info):
    with open(join(path, 'info_fullres.json'), 'w') as jfile:
        json.dump(info, jfile)

def ingest(path, parameters, destination):
    if not isdir(destination):
        makedirs(destination, 0o700)
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
    arguments = parser.parse_args()
    import ipdb; ipdb.set_trace()
    try:
        with open(arguments.definition) as df:
            definition = json.load(df)
    except Exception:
        sys.exit("Couldn't load definition file")
    print(definition)
    ingest(arguments.source, definition, arguments.destination)


if __name__ == "__main__":
    main()

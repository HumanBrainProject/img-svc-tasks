import argparse
import asyncio
import aioboto3
import aiofiles
import logging
import sys
import os
import re
import json
from botocore.config import Config

CREDENTIALS_LOCATION = './.ec2_creds'

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)

logger = logging.getLogger("send_results")

parser = argparse.ArgumentParser(description='Save results to Archival storage')
parser.add_argument('results', help='The local path to the results directory')
parser.add_argument('destination', help="The destination container")

def convert_filenames_to_labels(results_folder, filenames):
    '''
    Cut off results_folder from filename and  convert it into labels
    eg test/results/bigbrain/20um/5696-5760/3264-3328/64-100.gz > 20um/5696-5760_3264-3328_64-100
    '''

    # TODO not mathcing patterns are untouched and still have the
    # results_folder in the label

    pattern = re.compile(f'{results_folder}/(\w+/\d+-\d+)/(\d+-\d+)/(\d+-\d+).gz$')
    label = r'\1_\2_\3'
    import pdb; pdb.set_trace()
    return [re.sub(pattern, label, filename) for filename in filenames]

async def upload_results(results_folder, destination_container):
    # generate filelist from results folder
    files = [(os.path.join(dp, f)) for dp, dn, fn in os.walk(results_folder) for f in fn]
    labels = convert_filenames_to_labels(results_folder, files)
    with open(CREDENTIALS_LOCATION, 'r') as cf:
        credentials = json.load(cf)

    # !!!!
    # CUTTING IT SHORTER FOR TESTING
    files = files[:20]

    async with aioboto3.client(
        's3',
        'CH',
        endpoint_url='https://object.cscs.ch/',
        config=Config(signature_version='s3', s3={'addressing_style': 'path'}),
        **credentials) as client:
            for index, file in enumerate(files):
                async with aiofiles.open(file, 'rb') as fo:
                    await client.upload_fileobj(fo, destination_container, labels[index])



def main():
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(upload_results(args.results, args.destination))
    # res = boto3.resource('s3', 'CH', endpoint_url='https://object.cscs.ch/', config=Config(signature_version='s3', s3={'addressing_style': 'path'}))
    # client = boto3.client('s3', 'CH', endpoint_url='https://object.cscs.ch/', config=Config(signature_version=UNSIGNED, s3={'addressing_style': 'path'}))
    loop.close()

if __name__ == "__main__":
    main()

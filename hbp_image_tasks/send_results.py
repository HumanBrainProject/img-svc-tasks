import argparse
import asyncio
import aioboto3
import aiofiles
import logging
import sys
import os
from botocore.config import Config

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)

logger = logging.getLogger("fetch_input")

parser = argparse.ArgumentParser(description='Save results to Archival storage')
parser.add_argument('results', help='The local path to the results directory')
parser.add_argument('destination', help="The destination container")

async def upload_results(results_folder, destination_container):
    files = [os.path.join(dp, f) for dp, dn, fn in os.walk(results_folder) for f in fn]
    import pdb; pdb.set_trace()
    # TODO: labels are generated with './', such as
    # https://object.cscs.ch/img-svc-sample-output/./test/results/colin/1mm/128-151/0-64/64-128.gz?uploadId=MmFlMDJlYWQtNjNjMC00NzUwLTk0NWYtOWRhYzgzMjlmYWNi

    # async with aioboto3.client('s3', 'CH', endpoint_url='https://object.cscs.ch/', config=Config(signature_version='s3', s3={'addressing_style': 'path'})) as client:
    #     for file in files:
    #         async with aiofiles.open(file, 'rb') as fo:
    #             await client.upload_fileobj(fo, destination_container, file)



def main():
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(upload_results(args.results, args.destination))
    # res = boto3.resource('s3', 'CH', endpoint_url='https://object.cscs.ch/', config=Config(signature_version='s3', s3={'addressing_style': 'path'}))
    # client = boto3.client('s3', 'CH', endpoint_url='https://object.cscs.ch/', config=Config(signature_version=UNSIGNED, s3={'addressing_style': 'path'}))
    loop.close()

if __name__ == "__main__":
    main()

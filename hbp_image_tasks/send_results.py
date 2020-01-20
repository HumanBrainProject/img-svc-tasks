import argparse
import logging
import sys
import os
import re
import json
from time import perf_counter
from datetime import timedelta
from swiftclient.multithreading import OutputManager
from swiftclient.service import SwiftError, SwiftService, SwiftUploadObject


# S3 multithread
# http://ls.pwd.io/2013/06/parallel-s3-uploads-using-boto-and-threads-in-python/

CREDENTIALS_LOCATION = './.ec2_creds'

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)

logger = logging.getLogger("send_results")

parser = argparse.ArgumentParser(description='Save results to Archival storage')
parser.add_argument('results', help='The local path to the results directory')
parser.add_argument('destination', help="The destination container")

def convert_filenames_to_labels(results_folder, filepaths):
    '''
    Cut off results_folder from filename and  convert it into labels
    eg test/results/bigbrain/20um/5696-5760/3264-3328/64-100.gz > 20um/5696-5760_3264-3328_64-100
    '''

    # remove results_folder prefix from paths
    filenames = [path[len(results_folder):] for path in filepaths]
    pattern = re.compile(r'(\w+/\d+-\d+)/(\d+-\d+)/(\d+-\d+).gz$')
    label = r'\1_\2_\3'
    import ipdb; ipdb.set_trace()
    return [re.sub(pattern, label, filename) for filename in filenames]

def upload_results(results_folder, destination_container):
    # generate filelist from results folder
    files = [(os.path.join(dp, f)) for dp, dn, fn in os.walk(results_folder) for f in fn]
    labels = convert_filenames_to_labels(results_folder, files)
    # with open(CREDENTIALS_LOCATION, 'r') as cf:
    #     credentials = json.load(cf)


    # https://docs.openstack.org/python-swiftclient/latest/service-api.html#upload
    
    _opts = {'object_uu_threads': 20}
    with SwiftService(options=_opts) as swift, OutputManager() as out_manager:
        try:
            logger.info(f'Uploading {len(files)} objects to {destination_container}')
            start = perf_counter()
            objects = [SwiftUploadObject(file, object_name=labels[index] for index, file in enumerate(files)]
            swift.upload(destination_container, objects)
            finish = perf_counter()
            logger.info(f'Completed in {timedelta(seconds=finish-start)}')
        except SwiftError as e:
            logger.error(e.value)





def main():
    args = parser.parse_args()
    upload_results(args.results, args.destination)

if __name__ == "__main__":
    main()

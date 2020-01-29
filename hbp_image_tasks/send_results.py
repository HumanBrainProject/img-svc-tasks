import argparse
import logging
import sys
import os
import re
import json
from time import perf_counter
from datetime import timedelta
from shutil import rmtree
from swiftclient.multithreading import OutputManager
from swiftclient.service import SwiftError, SwiftService, SwiftUploadObject
from keystoneclient.v3 import client
from keystoneauth1 import session
from keystoneauth1.identity import v3
from keystoneauth1.extras._saml2 import V3Saml2Password

# S3 multithread
# http://ls.pwd.io/2013/06/parallel-s3-uploads-using-boto-and-threads-in-python/



logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)

# The following loggers are a bit too chatty by default
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("swiftclient").setLevel(logging.CRITICAL)

logger = logging.getLogger("send_results")



def get_keystone_token(settings):
    # GETTING UNSCOPED TOKEN
    # NEEDS LXML package
    auth = V3Saml2Password(
        identity_provider='cscskc',
        protocol='mapped',
        identity_provider_url='https://auth.cscs.ch/auth/realms/cscs/protocol/saml/',
        auth_url=settings["os_auth_url"],
        username=settings["os_username"],
        password=settings["os_password"])
    sess = session.Session(auth=auth)

    # GETTING PROJECT SCOPED TOKEN USING PREVIOUS TOKEN
    auth = v3.Token(
        auth_url=settings["os_auth_url"],
        token=sess.get_token(),
        project_id=settings["os_project_id"])
    sess = session.Session(auth=auth)
    return sess.get_token()

def convert_filenames_to_labels(results_folder, filepaths):
    '''
    Cut off results_folder from filename and  convert it into labels
    eg test/results/bigbrain/20um/5696-5760/3264-3328/64-100.gz > 20um/5696-5760_3264-3328_64-100
    '''

    # remove results_folder prefix from paths
    filenames = [path[len(results_folder):] for path in filepaths]
    pattern = re.compile(r'(\w+/\d+-\d+)/(\d+-\d+)/(\d+-\d+).gz$')
    label = r'\1_\2_\3'
    return [re.sub(pattern, label, filename) for filename in filenames]

def upload_results(results_folder, destination_container, cleanup):
    SETTINGS_LOCATION = os.environ.get('SWIFT_SETTINGS')
    if not SETTINGS_LOCATION:
        sys.exit("No OpenStack settings provided for the upload")
    with open(SETTINGS_LOCATION, 'r') as sf:
        settings = json.load(sf)

    # generate filelist from results folder
    files = [(os.path.join(dp, f)) for dp, dn, fn in os.walk(results_folder) for f in fn]
    labels = convert_filenames_to_labels(results_folder, files)

    options = {'object_uu_threads': 20,
               'os_auth_token': get_keystone_token(settings)}
    # Remove password from the OpenStack settings, otherwise the SwiftService
    # connection will be built ignoring the token and failing authentication
    del(settings['os_password'])
    options.update(**settings)

    with SwiftService(options=options) as swift, OutputManager() as out_manager:
        try:
            logger.info(F'Making public container {destination_container}')
            swift.post(container=destination_container, options={'read_acl': '.r:*,.rlistings'})
            logger.info(f'Uploading {len(files)} objects to {destination_container}')
            start = perf_counter()
            objects = [SwiftUploadObject(file, object_name=labels[index]) for index, file in enumerate(files)]
            for result in swift.upload(destination_container, objects):
                if not result['success']:
                    logger.error(f"Failed to upload object")
                    sys.exit("Failed to upload object")
            finish = perf_counter()
            logger.info(f'Completed in {timedelta(seconds=finish-start)}')
        except SwiftError as e:
            logger.exception(e.value)
            sys.exit("Failed to upload objects")

    if cleanup:
        logging.info("Deleting results folder")
        rmtree(results_folder)
        logging.info("Done")



def main():
    parser = argparse.ArgumentParser(description='Save results to Archival storage')
    parser.add_argument('results', help='The local path to the results directory')
    parser.add_argument('destination', help="The destination container")
    parser.add_argument('--cleanup',  action='store_true',
        help="Wipe the local chunks after a successful upload")
    args = parser.parse_args()
    upload_results(args.results, args.destination, args.cleanup)

if __name__ == "__main__":
    main()

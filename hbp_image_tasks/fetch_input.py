import argparse
import asyncio
import aiohttp
import aiofiles
import re
import sys
import logging
from time import perf_counter
from datetime import timedelta
from urllib.parse import urljoin
from os import getcwd, makedirs
from os.path import isdir, join
# from botocore.config import Config



logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)

logger = logging.getLogger("fetch_input")


async def download_file(session, object_url, destination):
    # import pdb; pdb.set_trace()
    async with session.get(object_url) as resp:
        if resp.status == 200:
            filepath = join(destination, object_url.split('/')[-1])
            async with aiofiles.open(filepath, "wb") as f:
                await f.write(await resp.read())
        else:
            resp.raise_for_status()

async def download(source, stacks, regex, destination):
    connector = aiohttp.TCPConnector(limit=40)
    if regex:
        pattern = re.compile(regex)
    async with aiohttp.ClientSession(connector=connector) as session:
        if stacks:
            if source[-1] != '/':
                source = f"{source}/"
            async with session.get(source) as resp:
                objects = (await resp.text()).split()
                downloads = list(filter(lambda obj: re.match(pattern, obj) is not None, objects))

                # url = urljoin(source, results[0])
        else:
            downloads = [source]
        logger.info("Downloading {0} tiles:[\n {1}]".format(len(downloads), ' '.join(downloads)))
        await asyncio.gather(*[download_file(session, urljoin(source, object), destination) for object in downloads])

def fetch_input(source, stacks, filter, destination):
    if not isdir(destination):
        makedirs(destination, 0o700)
    loop = asyncio.get_event_loop()
    start = perf_counter()
    loop.run_until_complete(download(source, stacks, filter, destination))
    finish = perf_counter()
    logger.info(f'Download completed in {timedelta(seconds=finish-start)}')
    loop.close()

def main():
    parser = argparse.ArgumentParser(description='Fetch input data for processing')
    parser.add_argument('source', help='The source url in http')
    parser.add_argument('--stacks', action='store_true', help='Whether ther are stack under the URL')
    parser.add_argument('--filter', help="Filename filter regex for container stacks")
    parser.add_argument('--destination', default=getcwd(), help="Destination directory")
    args = parser.parse_args()
    fetch_input(args.source, args.stacks, args.filter, args.destination)


if __name__ == "__main__":
    main()

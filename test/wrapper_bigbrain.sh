#!/bin/bash

set -e

NAME='bigbrain'
SOURCE="./source/$NAME"
RESULTS="./results/$NAME"
PARAMS='{"num_channels": 1, "type": "image", "data_type": "uint8", "scales": [{"encoding": "raw", "chunk_sizes": [], "key": "full", "resolution": [21166.666666666668, 20000, 21166.666666666668], "voxel_offset": [0, 0, 0], "size": [6572, 5711, 100]}]}'

if [ -d $SOURCE ]; then
  rm -r $SOURCE
fi

if [ -d $RESULTS ]; then
  rm -r $RESULTS
fi

mkdir -p $SOURCE
mkdir -p $RESULTS


SWIFT_SETTINGS='../.os_settings' ingest \
  --source https://object.cscs.ch/v1/AUTH_61499a61052f419abad475045aaf88f9/img-svc-bigbrain-input \
  --download-dir $SOURCE \
  --results-dir $RESULTS \
  --stacks \
  --filter 'data/raw/original/pm31\d{2}o.png' \
  --parameters "$PARAMS" \
  --container test_wrapper \
  --noupload \
  --cleanup

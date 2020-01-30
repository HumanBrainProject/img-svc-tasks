#!/bin/bash

set -e

NAME='bigbrain'
SOURCE="./source/$NAME"
RESULTS="./results/$NAME"
PARAMS='{"num_channels": 1, "type": "image", "data_type": "uint8", "scales": [{"encoding": "raw", "chunk_sizes": [], "key": "full", "resolution": [20000, 20000, 20000], "voxel_offset": [0, 0, 0], "size": [1376, 623, 815]}]}'


if [ -d $SOURCE ]; then
  rm -r $SOURCE
fi

if [ -d $RESULTS ]; then
  rm -r $RESULTS
fi

mkdir -p $SOURCE
mkdir -p $RESULTS


SWIFT_SETTINGS='../.os_settings' ingest \
  --source https://object.cscs.ch/v1/AUTH_63ea6845b1d34ad7a43c8158d9572867/Pavone_RUP_T1.2.2/ \
  --download-dir $SOURCE \
  --results-dir $RESULTS \
  --stacks \
  --filter 'hbp-00020/hippoDS/hippo-1/dorsal/hbp-00020_hippoDS_hippo-1_dorsal__s0[0-9]{3}.tif' \
  --parameters "$PARAMS" \
  --container test_kg-1 \
  --noupload

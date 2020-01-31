#!/bin/bash

set -e

NAME='colin'
SOURCE="./source/$NAME"
RESULTS="./results/$NAME"
PARAMS='{"data_type": "uint8"}'

if [ -d $SOURCE ]; then
  rm -r $SOURCE
fi

if [ -d $RESULTS ]; then
  rm -r $RESULTS
fi

mkdir -p $SOURCE
mkdir -p $RESULTS


SWIFT_SETTINGS='../.os_settings' ingest \
  --source https://github.com/HumanBrainProject/neuroglancer-scripts/raw/master/examples/JuBrain/colin27T1_seg.nii.gz \
  --download-dir $SOURCE \
  --results-dir $RESULTS \
  --parameters "$PARAMS" \
  --container test_colin \
  --noupload \
  --cleanup

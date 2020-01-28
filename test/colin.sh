#!/bin/bash
set -e
# Testing task chain for single file


NAME='colin'
SOURCE="./source/$NAME"
RESULTS="./results/$NAME"

if [ -d $SOURCE ]; then
  rm -r $SOURCE
fi

if [ -d $RESULTS ]; then
  rm -r $RESULTS
fi

mkdir -p $SOURCE
mkdir -p $RESULTS


fetch_input \
  https://github.com/HumanBrainProject/neuroglancer-scripts/raw/master/examples/JuBrain/colin27T1_seg.nii.gz \
  --destination $SOURCE

ingest \
  $SOURCE/colin27T1_seg.nii.gz \
  ./definitions/colin.json \
  --destination $RESULTS

SWIFT_SETTINGS=../.os_settings send_results \
  $RESULTS \
  test_colin \
  --cleanup

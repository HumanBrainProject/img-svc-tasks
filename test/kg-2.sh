#!/bin/bash

NAME='kg-2'
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


# fetch_input \
#   --stacks https://object.cscs.ch/v1/AUTH_227176556f3c4bb38df9feea4b91200c/hbp-data-000326 \
#   --filter 'mosaic1/fused.tiff' \
#   --destination $SOURCE

ingest \
  $SOURCE \
  ./definitions/$NAME.json \
  --destination $RESULTS

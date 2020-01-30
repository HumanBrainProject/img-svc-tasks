#!/bin/bash

NAME='kg-3'
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
  https://object.cscs.ch/v1/AUTH_63ea6845b1d34ad7a43c8158d9572867/Pavone_RUP_T1.2.2/ \
  --stacks \
  --filter 'hbp-00020/hippoDS/hippo-1/dorsal/hbp-00020_hippoDS_hippo-1_dorsal__s0[0-9]{3}.tif' \
  --destination $SOURCE

ingest_ngs \
  $SOURCE \
  --definition-file ./definitions/$NAME.json \
  --destination $RESULTS

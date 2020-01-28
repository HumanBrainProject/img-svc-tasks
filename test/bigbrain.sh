#!/bin/bash

set -e

NAME='bigbrain'
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
  --stacks https://object.cscs.ch/v1/AUTH_61499a61052f419abad475045aaf88f9/img-svc-bigbrain-input \
  --filter 'data/raw/original/pm31\d{2}o.png' \
  --destination $SOURCE

ingest \
  $SOURCE \
  ./definitions/bigbrain_ingest.json \
  --destination $RESULTS

SWIFT_SETTINGS=../.os_settings send_results \
  $RESULTS \
  test_bigbrain \
  --cleanup

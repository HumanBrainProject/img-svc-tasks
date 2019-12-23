#!/bin/bash

NAME='kg-1'
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
  --stacks https://object.cscs.ch/v1/AUTH_6ebec77683fb472f94d352be92b5a577/tTA-atlas \
  --filter 'CamKII-tTA-coronal-case317_8/317_8_CaMKII_tiffs/317_8_CamKII_tTA_lacZ_Xgal_s1[8-9][0-9]_1.4.tif' \
  --destination $SOURCE

ingest \
  $SOURCE \
  ./definitions/kg-1.json \
  --destination $RESULTS

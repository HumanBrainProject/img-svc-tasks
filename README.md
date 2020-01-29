# Tasks that can be invoked by the Image Service on the HPC signature_version

# Main wrapper script

## `ingest`

Combines arguments from the other sub-modules and does all steps  in on script.

Example

```
SWIFT_SETTINGS='../.os_settings' ingest \
  --source https://object.cscs.ch/v1/AUTH_61499a61052f419abad475045aaf88f9/img-svc-bigbrain-input \
  --download-dir $SOURCE \
  --results-dir $RESULTS \
  --stacks \
  --filter 'data/raw/original/pm31\d{2}o.png' \
  --parameters "$PARAMS" \
  --container test_wrapper2 \
  --cleanup
```


# Modules

## `fetch_input`

  Examples:

  * Stacks

  ```
  fetch_input \
    --stacks \
    --filter 'Pitx3-tTA-horizontal-case6513/6513_PitX3_tiffs/6513_Pitx3_tTA_lacZ_Xgal_s01\d_0.22.tif' \
    --destination ./source \
    https://object.cscs.ch/v1/AUTH_6ebec77683fb472f94d352be92b5a577/tTA-atlas
  ```

  * Single files

  ```
  fetch_input \
    --destination ./source \
    https://github.com/HumanBrainProject/neuroglancer-scripts/raw/master/examples/JuBrain/colin27T1_seg.nii.gz
  ```


## `ingest_ngs`

Chunk up input data using the neuroglancer_scripts



## `upload_results`

Uploads the results to a SWIFT container.

Expects a JSON file with SWIFT settings, example:

```
{
  "auth_version": "3",
  "os_username": "username",
  "os_password": "password",
  "os_project_id": "08c08f9f119744cbbf77e216988da3eb",
  "os_auth_url": "https://pollux.cscs.ch:13000/v3".
  "os_storage_url": "https://object.cscs.ch/v1/AUTH_08c08f9f119744cbbf77e216988da3eb"
}
```

# Tasks that can be invoked by the Image Service on the HPC signature_version

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


## `send_results`

Uploads the results to a SWIFT container using the S3 API.

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

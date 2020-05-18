# Tasks that can be invoked by the Image Service on the HPC workers

# Scripts in the package

## `ingest`

Combines arguments from the other sub-modules and does all steps in one
Command Line Interface.

It has the advantage of executing a complete process with a single Unicore job
definition.

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


## `fetch_input`

  Fetches the input data for processing.
  * Can be a single URL which does not require authentication.
  * In case it's a stack of images, a CSCS Swift container and an option regex
  filter for objects in this container is also accepted.

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

Chunk up the input data using the neuroglancer_scripts

## `upload_results`

Uploads the results to a SWIFT container.

Expects a JSON file with SWIFT settings.

**IMPORTANT**  When this file is deployed to the HPC
make sure it is kept in a service accounts's home folder and the file itself
is only readable by that specific user (`chmod 0600`)!!!

YOU DO NOT WANT TO SHARE THESE CREDENTIALS WITH OTHERS.

Example:

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

# Deployment

Manual operation for now.

* Build a source distribution,
  * `python setup.py sdist`
* then copy it to the HPC cluster,
  * ```
    VERSION=$(grep version setup.py | cut -d= -f2 | cut -d\' -f2) \
    PKG=hbp-image-tasks-$VERSION.tar.gz \
    rsync -av \
      dist/$PKG \
      ich019sa@ela.cscs.ch:~
    ```
* finally install it to the existing virtualenv
  * SSH to ela.cscs.ch
  * SSH to daint.cscs.ch (no Python on ela)
  * activate virtualenv and install package.
    * `/store/hbp/ich019/img-svc-tasks/bin/pip install /users/ich019sa/hbp-image-tasks-0.0.1.tar.gz`

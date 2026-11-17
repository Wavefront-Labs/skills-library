---
id: computing-software.ai-ml-engineering.litellm.litellm-config-from-env-or-bucket
name: litellm-config-from-env-or-bucket
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, config-file-path, s3-config, gcs-config]
level: practitioner
status: docs-checked
description: "Start the proxy from CONFIG_FILE_PATH, or read config.yaml from an S3 or GCS bucket when you cannot mount a file."
sources:
  - https://docs.litellm.ai/docs/proxy/configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: start the proxy without a config file argument, by pointing it at a file with an environment variable or at an object in a bucket.
CONFIG_FILE_PATH (easier Azure container deployment):

```
CONFIG_FILE_PATH="/path/to/config.yaml"
litellm
# RUNNING on http://0.0.0.0:4000
```

Config from a bucket: use this when you cannot mount a config file on your deployment service (for example AWS Fargate or Railway). The proxy reads config.yaml from an S3 or GCS object.

GCS:

```
LITELLM_CONFIG_BUCKET_TYPE = "gcs"
LITELLM_CONFIG_BUCKET_NAME = "litellm-proxy"
LITELLM_CONFIG_BUCKET_OBJECT_KEY = "proxy_config.yaml"
```

```
docker run --name litellm-proxy \
   -e DATABASE_URL=<database_url> \
   -e LITELLM_CONFIG_BUCKET_NAME=<bucket_name> \
   -e LITELLM_CONFIG_BUCKET_OBJECT_KEY="<object_key>" \
   -e LITELLM_CONFIG_BUCKET_TYPE="gcs" \
   -p 4000:4000 \
   docker.litellm.ai/berriai/litellm:latest --detailed_debug
```

S3: set only the bucket name and object key (the type variable is for GCS):

```
LITELLM_CONFIG_BUCKET_NAME = "litellm-proxy"
LITELLM_CONFIG_BUCKET_OBJECT_KEY = "litellm_proxy_config.yaml"
```

Then run the same docker command without LITELLM_CONFIG_BUCKET_TYPE.

The container image is `docker.litellm.ai/berriai/litellm:latest`.

Enterprise features: set `LITELLM_LICENSE="eyJ..."` (a JWT from your Enterprise purchase) in the environment or .env; LiteLLM detects it and activates them.

## Checked

2026-11-03. Confirmed on the LiteLLM proxy config page (docs.litellm.ai/docs/proxy/configs): CONFIG_FILE_PATH, the LITELLM_CONFIG_BUCKET_* variables for GCS and S3, the Fargate/Railway use case, the docker run example and LITELLM_LICENSE. Removed an unconfirmed closing sentence.

Method: documentation only; no commands were run.

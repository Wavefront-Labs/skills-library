---
id: computing-software.ai-ml-engineering.open-webui.set-up-s3-file-storage
name: set-up-s3-file-storage
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [s3-storage, storage-provider, s3, minio, object-storage]
level: practitioner
status: docs-checked
description: "Switch Open WebUI uploads from local disk to Amazon S3 or an S3-compatible service using STORAGE_PROVIDER and the S3_* variables, then verify an upload."
sources:
  - https://docs.openwebui.com/tutorials/maintenance/s3-storage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: store uploaded files in S3 instead of `/app/backend/data/uploads`. (Community tutorial, not supported by the Open WebUI team.)

## Variables
- `STORAGE_PROVIDER`: `local` (default), `s3`, `gcs`, `azure`. Lowercase, matched exactly; an empty or unknown value stops startup with "Unsupported storage provider". Azure uses `AZURE_STORAGE_ENDPOINT`, `AZURE_STORAGE_CONTAINER_NAME`, plus `AZURE_STORAGE_KEY` or the default Azure credential.
- `S3_BUCKET_NAME`: the only strictly required S3 variable; `S3_REGION_NAME` is normally needed too.
- `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`: if omitted, the default AWS credential chain (for example an IAM role) is used.
- `S3_ENDPOINT_URL`: only needed for S3-compatible services (for example `https://s3.us-east-1.amazonaws.com` as the AWS example).
- Also available: `S3_KEY_PREFIX`, `S3_ADDRESSING_STYLE` (`path` for MinIO-style endpoints), `S3_USE_ACCELERATE_ENDPOINT`, `S3_ENABLE_TAGGING`.

Prerequisites: an AWS account, credentials, and IAM permission to create and put objects.

## Run
```sh
docker run -d -p 3000:8080 -v open-webui:/app/backend/data \
  -e STORAGE_PROVIDER="s3" \
  -e S3_ACCESS_KEY_ID="ABC123" \
  -e S3_SECRET_ACCESS_KEY="SuperSecret" \
  -e S3_ENDPOINT_URL="https://s3.us-east-1.amazonaws.com" \
  -e S3_REGION_NAME="us-east-1" \
  -e S3_BUCKET_NAME="my-awesome-bucket-name" \
  -e ENV="dev" \
  --name open-webui ghcr.io/open-webui/open-webui:main
```
`ENV=dev` exposes the Swagger docs so you can inspect files.

## Verify
Upload a small text file in a chat and confirm the model answers. In the bucket there is now an object named `<file-id>_hello.txt` (under `S3_KEY_PREFIX` if set). With Swagger, `GET /api/v1/files/{id}` returns the record for that id.

## Gotchas
- With `s3`, every upload is first written to `/app/backend/data/uploads` and then copied to the bucket, and each read downloads the object back there. The local data volume is still required.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: tutorials/maintenance/s3-storage (read in full). Removed: the omit-in-production advice, the slim-image claim and the migration remark, none of which the page states.
Method: documentation only; no commands were run.

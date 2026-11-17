---
id: computing-software.cybersecurity-defensive.pomerium.recording-blob-gcs-s3
name: recording-blob-gcs-s3
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [blob-storage, bucket-uri, gcs-bucket, s3-bucket, recording-datasource]
level: advanced
status: docs-checked
description: "Configure Pomerium session recording storage on GCS or S3: bucket URI format, credentials, permissions and S3-compatible server parameters."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/session-recording/storage.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Blob URI format: `<scheme>://<bucket>?<param1>=<value1>&...`. Credentials are not shared from Enterprise to Core; configure each instance. Create the datasource in the same namespace as the cluster (Console Datasources page, or Terraform `pomerium_recording_data_source` plus `blob_storage.bucket_uri` in `pomerium_settings`).

**GCS** `gs://<bucket-name>`
- Application Default Credentials, or `GOOGLE_APPLICATION_CREDENTIALS`. On Cloud Run the service account is used.
- Uploader: Storage Object Creator and Viewer. Enterprise: Storage Object Viewer.
- Params: `anonymous`, `access_id`, `private_key_path`, `universe_domain`.

**S3** `s3://<bucket-name>`
- Credentials file via `AWS_SHARED_CREDENTIALS_FILE` or `AWS_CONFIG_FILE` (default `~/.aws/credentials`), selected with `?profile=<name>`; on EC2 use an instance profile.
- Params: `ssetype` (`AES256`, `aws:kms`, `aws:kms:dsse`), `kmskeyid`, `accelerate`, `use_path_style`, `s3ForcePathStyle`, `disable_https`, `profile`.
- S3-compatible (Minio, Ceph, SeaweedFS): `s3://mybucket?endpoint=http://my.minio.local:8080&disable_https=true&s3ForcePathStyle=true`. A region is still needed; `us-east-1` is the suggested placeholder.

Recordings may hold privileged data: enable encryption, integrity and object locking per your provider's documentation. See recording-blob-azure-file for Azure and file stores.

## Checked

2026-11-04. Read the Session Recording Storage page: URI format, per-instance credentials, datasource namespace rule, GCS credentials, roles and parameters, S3 credential file, profile parameter, parameters list, and the S3-compatible example and region note all confirmed. Nothing removed.

Method: documentation only; no commands were run.

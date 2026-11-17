---
id: computing-software.cybersecurity-defensive.pomerium.recording-blob-azure-file
name: recording-blob-azure-file
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [azure-blob, azblob, file-storage, object-layout, recording-metadata]
level: advanced
status: docs-checked
description: "Configure Azure and file storage for Pomerium session recordings and read the stored object layout and captured metadata."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/session-recording/storage.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Azure** `azblob://<container-name>`
- Credentials, one of: account key (`AZURE_STORAGE_KEY` base64 plus `AZURE_STORAGE_ACCOUNT`); SAS token (`AZURE_STORAGE_ACCOUNT` and `AZURE_STORAGE_SAS_TOKEN`); connection string (`AZURE_STORAGE_CONNECTION_STRING`, plus the account variable if absent); service principal (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, and `AZURE_CLIENT_SECRET` or `AZURE_CLIENT_CERTIFICATE_PATH`).
- Params: `domain`, `protocol` (`http` or default `https`), `cdn`, `localemu` (for Azurite).

**File** `file://<file-path>`: not recommended for production; Enterprise can replay only if it runs on the same host as the writers. Params: `create_dir`, `dir_file_mode` (default `0777`), `no_tmp_dir`, `base_url`, `secret_key_path`, `metadata` (`"skip"`).

**Object layout**: `<pomerium-cluster-id>/ssh/v1/<recording-id>/` containing `manifest`, `metadata.json`, `metadata.proto`, `recording_0000000000` and further chunks, and `signature` (currently the full Pomerium version). Recording chunks are protobuf.

**Captured metadata**: `start_time`, `login_name`, `session_id`, `user_id`, `stream_id`, `route_name` (for `ssh://example`, `example`), `upstream` (for `ssh://0.0.0.0:22`, `0.0.0.0:22`), `pty_info`.

See recording-blob-gcs-s3 for GCS and S3.

## Checked

2026-11-04. Read the Session Recording Storage page: Azure credential variants and parameters, file storage warning and parameters, object layout, signature contents and captured metadata fields all confirmed. Nothing removed.

Method: documentation only; no commands were run.

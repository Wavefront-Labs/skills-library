---
id: computing-software.collaboration-platform-administration.zulip.s3-upload-backend-setup
name: s3-upload-backend-setup
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [s3-uploads, upload-backend, s3-auth-uploads-bucket, max-file-upload-size]
level: practitioner
status: docs-checked
description: "Switch Zulip file uploads to S3 or S3-compatible storage: two buckets, s3_key secrets, S3_AUTH_UPLOADS_BUCKET, S3_AVATAR_BUCKET, endpoint, region, checksum and GCS gcp_key.json."
sources: ["https://zulip.readthedocs.io/en/latest/production/upload-backends.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# S3 file upload backend

By default Zulip stores uploads (message files, avatars, organization icons, custom emoji) on disk under `LOCAL_UPLOADS_DIR`, which neither scales nor works with multiple servers. `MAX_FILE_UPLOAD_SIZE` caps file size for any backend; 0 disables uploads and hides the upload UI.

To enable S3:

1. In AWS, create an IAM user for Zulip and two buckets: one for uploaded files and one for user avatars. They must be separate because the avatar bucket is world-readable and the uploads bucket is not.
2. Put `s3_key` and `s3_secret_key` in `/etc/zulip/zulip-secrets.conf`, or on EC2 give the instance the IAM role.
3. In `/etc/zulip/settings.py` set `S3_AUTH_UPLOADS_BUCKET` and `S3_AVATAR_BUCKET`.
4. Comment out `LOCAL_UPLOADS_DIR`.
5. For non-AWS providers set `S3_ENDPOINT_URL`; some AWS regions need `S3_REGION`, such as `"eu-central-1"`.
6. Non-AWS providers may need `S3_SKIP_CHECKSUM = True`; try without first, and enable it if you see `XAmzContentSHA256Mismatch` exceptions.
7. Restart with `~zulip/deployments/current/scripts/restart-server`.

Existing files are not uploaded by this process.

Google Cloud Storage: set the bucket names, `S3_ENDPOINT_URL = "https://storage.googleapis.com"` and `S3_SKIP_CHECKSUM = True`, add the S3-style keys, and also create `/etc/zulip/gcp_key.json` holding a service account key with "Storage Object Admin" on the uploads bucket. The tusd chunked-upload service uses it.

Docker users supply `SETTING_S3_*` variables and the `s3_key` and `s3_secret_key` secrets.

## Checked

2026-11-08. Checked: read against the Zulip upload-backends page (docs/production/upload-backends.md, read in full). Removed: nothing.

Method: documentation only; no commands were run.

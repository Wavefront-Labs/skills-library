---
id: computing-software.collaboration-platform-administration.zulip.migrate-local-uploads-to-s3
name: migrate-local-uploads-to-s3
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [transfer-uploads-to-s3, uploads-migration, local-uploads-dir]
level: practitioner
status: docs-checked
description: "Move existing Zulip uploads from LOCAL_UPLOADS_DIR to S3 with manage.py transfer_uploads_to_s3, its processes option, cutover order and the avatar caveat."
sources: ["https://zulip.readthedocs.io/en/latest/production/upload-backends.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migrating local uploads to S3

Switching the settings alone does not copy existing files, so migrate before cutting over.

1. Configure the S3 backend as usual: keys in `/etc/zulip/zulip-secrets.conf`, bucket names, endpoint and region in `/etc/zulip/settings.py`. Leave `LOCAL_UPLOADS_DIR` set, since the migration tool uses it to locate your current files.
2. Run, from the current deployment:

```
./manage.py transfer_uploads_to_s3
```

It uploads everything from the local directory to S3. Uploading is latency-sensitive, so it uses 6 parallel processes by default; change this with `--processes`.

3. When the script finishes, comment out `LOCAL_UPLOADS_DIR` and restart the server with `~zulip/deployments/current/scripts/restart-server`.

Caveat: the tool does not migrate an uploaded organization avatar or logo.

The local backend is simple but does not work with multiple Zulip servers and does not scale. `MAX_FILE_UPLOAD_SIZE` applies to every backend.

## Checked

2026-11-08. Checked: read against the Zulip upload-backends page (docs/production/upload-backends.md, read in full). Removed: advice to re-upload organization avatars and a scalability-guidance claim about warm spares, neither on the page.

Method: documentation only; no commands were run.

---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-uploads-and-storage
name: bookstack-uploads-and-storage
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, file-upload-size-limit, storage-type, s3, local-secure, attachments, client-max-body-size, php-ini]
level: practitioner
status: docs-checked
description: "Configure BookStack uploads: FILE_UPLOAD_SIZE_LIMIT with matching PHP and nginx limits, STORAGE_TYPE local, local_secure, local_secure_restricted and S3, and S3 variables."
sources: ["https://www.bookstackapp.com/docs/admin/upload-config/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack uploads and storage

Size limits must be raised in every layer:

- BookStack: `FILE_UPLOAD_SIZE_LIMIT=50` (megabytes) in `.env`.
- PHP `php.ini`: `post_max_size` and `upload_max_filesize` (docs suggest 10M unless more is needed); `memory_limit` such as 256M for files over 128 MB.
- Nginx: `client_max_body_size` (default 1MB) and perhaps `client_body_timeout` (default 60s).
- Apache has no built-in limit; with mod_php use `php_value` in `.htaccess`.

`STORAGE_TYPE`:
- `local` (default): images public, attachments guarded by BookStack permissions.
- `local_secure`: images require login unless public access is on.
- `local_secure_restricted`: image access follows permissions of the page it was uploaded to.
- `s3`: Amazon S3 or compatible; images are made public on upload.

S3 variables: `STORAGE_S3_KEY`, `STORAGE_S3_SECRET`, `STORAGE_S3_BUCKET`, `STORAGE_S3_REGION`, `STORAGE_S3_ENDPOINT` (non-Amazon), optional `STORAGE_URL` base. `STORAGE_ATTACHMENT_TYPE` and `STORAGE_IMAGE_TYPE` set attachment and image storage separately; both default to `STORAGE_TYPE`, with `local` forced to `local_secure` for attachments.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) admin/upload-config/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: nothing.
Method: documentation only; no commands were run.

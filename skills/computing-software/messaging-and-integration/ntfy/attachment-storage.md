---
id: computing-software.messaging-and-integration.ntfy.attachment-storage
name: attachment-storage
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, attachments, attachment-cache-dir, s3, storage]
level: practitioner
status: docs-checked
description: "Enable attachments on a self-hosted ntfy server with a filesystem directory or an S3 bucket, and set size, expiry and bandwidth limits."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attachment storage

```yaml
base-url: "https://ntfy.example.com"
attachment-cache-dir: "/var/cache/ntfy/attachments"
attachment-total-size-limit: "5G"
attachment-file-size-limit: "15M"
attachment-expiry-duration: "3h"
visitor-attachment-total-size-limit: "100M"
visitor-attachment-daily-bandwidth-limit: "500M"
```

Defaults: total 5G, per file 15M, expiry 3h. Expiry is capped at `cache-duration`. `base-url` is required.

## S3

```
attachment-cache-dir: "s3://ACCESS_KEY:SECRET_KEY@my-bucket/attachments?region=us-east-1"
```

Format: `s3://ACCESS_KEY:SECRET_KEY@BUCKET[/PREFIX]?region=REGION[&endpoint=ENDPOINT][&disable_http2=true]`.

- URL-encode keys with special characters (`+` becomes `%2B`).
- Add `&disable_http2=true` if you hit HTTP/2 stream errors.
- Warning: ntfy takes full control of the directory or bucket.

## Gotchas

- The page's nginx example sets `client_max_body_size 0` to stream the request body to the backend.
- Attachments need a storage backend (`attachment-cache-dir`) and `base-url`.

## Checked

2026-11-04. Confirmed against the ntfy config page (Attachments, S3 storage, nginx example): options and defaults (5G, 15M, 3h), expiry cap at `cache-duration`, S3 URL format, URL-encoding, `disable_http2`, full-control warning, visitor limit options. Removed: the Verify step and the claim that uploads fail without the nginx setting.
Method: documentation only; no commands were run.

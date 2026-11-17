---
id: computing-software.messaging-and-integration.ntfy.attachments-local-file
name: attachments-local-file
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, attachments, upload, x-filename, put]
level: practitioner
status: docs-checked
description: "Attach a local file to an ntfy notification by PUTting it as the body, with X-Filename, and know the size and expiry limits."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attaching a local file

Send the file as the request body:

```
curl -T flower.jpg -H "Filename: flower.jpg" ntfy.sh/flowers
```

- `X-Filename` has aliases `Filename`, `File`, `f`.
- Messages over 4,096 bytes, or with non-UTF-8 content, are sent as attachments automatically. Smaller text-only files need the filename header to be treated as attachments.

## Limits

- Default config (as the publish page describes ntfy.sh): 15 MB per attachment, 100 MB total per visitor, expiry after 3 hours.
- The page's limits table says that on ntfy.sh itself the attachment size limit is 2 MB with 20 MB per visitor; check the current limits.

Self-hosted defaults come from `attachment-file-size-limit` (15M), `attachment-total-size-limit` (5G), `attachment-expiry-duration` (3h) and the visitor limits; see the attachment-storage skill. Attachments need `attachment-cache-dir` and `base-url` set on the server.

## Gotchas

- Expiry is capped at `cache-duration`.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Attach local file, limits table) and the config page (attachment options): PUT body, 4,096-byte threshold, filename aliases, defaults, expiry cap. Corrected: the ntfy.sh limit figures, which the page states inconsistently. Removed: an expiry gotcha and the Verify step.
Method: documentation only; no commands were run.

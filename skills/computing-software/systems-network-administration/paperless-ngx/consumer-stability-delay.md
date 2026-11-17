---
id: computing-software.systems-network-administration.paperless-ngx.consumer-stability-delay
name: consumer-stability-delay
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, stability-delay, filenotfounderror, consumer, scanner, paperless-consumer-stability-delay]
level: practitioner
status: docs-checked
description: "Stop FileNotFoundError and half-written file consumption by raising PAPERLESS_CONSUMER_STABILITY_DELAY, and map the old v2 consumer settings."
sources:
  - "https://docs.paperless-ngx.com/troubleshooting/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/migration-v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consumer stability delay

## Symptom
```
Error while consuming document SCN_0001.pdf: FileNotFoundError: [Errno 2] No such file or directory: '/tmp/ocrmypdf.io.../origin.pdf'
```
This usually means the same file was consumed twice, or consumed while still being written, which happens when a scanner modifies a file several times.

## Fix
`PAPERLESS_CONSUMER_STABILITY_DELAY` is how many seconds a file must keep the same size and modification time before consumption starts. The default is 5.0. Raise it for slow network storage or awkward scanners:
```bash
PAPERLESS_CONSUMER_STABILITY_DELAY=15
```

## v3 mapping
v3 uses the watchfiles library, so several settings changed:
- `CONSUMER_POLLING` is now `CONSUMER_POLLING_INTERVAL`.
- `CONSUMER_INOTIFY_DELAY` is now `CONSUMER_STABILITY_DELAY`, used in every mode.
- `CONSUMER_POLLING_DELAY` and `CONSUMER_POLLING_RETRY_COUNT` are removed.
- `CONSUMER_IGNORE_PATTERNS` now holds regexes, not fnmatch patterns, and adds to the defaults.
- `CONSUMER_IGNORE_DIRS` is new.

## Other causes
Pre-consume scripts that edit the original path can trigger a second consume task. Edit only `DOCUMENT_WORKING_PATH`.

If the consumer finds nothing at all, check the folder mapping, the broker and the task worker.

## Checked
2026-11-04. Compared with the FileNotFoundError entry of troubleshooting, PAPERLESS_CONSUMER_STABILITY_DELAY in configuration, the consumer settings table of the v3 migration page, and the pre-consume note of advanced_usage (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: the error text, default 5.0, same size and modification time rule, all five setting mappings, the pre-consume script cause, the no-files checklist. Nothing removed.

Method: documentation only; no commands were run.

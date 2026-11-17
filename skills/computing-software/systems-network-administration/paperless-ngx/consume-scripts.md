---
id: computing-software.systems-network-administration.paperless-ngx.consume-scripts
name: consume-scripts
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, pre-consume-script, post-consume-script, hooks, document-working-path, consume-hooks]
level: advanced
status: docs-checked
description: "Run your own scripts before or after consumption with environment variables only, mount them in Docker and avoid v3 positional argument breakage."
sources:
  - "https://docs.paperless-ngx.com/advanced_usage/"
  - "https://docs.paperless-ngx.com/migration-v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre and post consumption scripts

Set `PAPERLESS_PRE_CONSUME_SCRIPT` or `PAPERLESS_POST_CONSUME_SCRIPT` to an executable path. Scripts run blocking, so slow ones delay consumption; fork and exit to run asynchronously. Output and exit code are logged.

## Pre-consume
Runs after the file is seen, before processing. Variables: `DOCUMENT_SOURCE_PATH`, `DOCUMENT_WORKING_PATH` (the copy consumption works on) and `TASK_ID`. Modify only `DOCUMENT_WORKING_PATH`, otherwise a second consume task can start on the same path. Non-deterministic edits may let duplicates in.
```bash
#!/usr/bin/env bash
pdf2pdfocr.py -i "${DOCUMENT_WORKING_PATH}"
```

## Post-consume
Runs after the document is in Paperless. Variables include `DOCUMENT_ID`, `DOCUMENT_FILE_NAME`, `DOCUMENT_TYPE`, `DOCUMENT_CREATED`, `DOCUMENT_ADDED`, `DOCUMENT_SOURCE_PATH`, `DOCUMENT_ARCHIVE_PATH`, `DOCUMENT_THUMBNAIL_PATH`, `DOCUMENT_DOWNLOAD_URL`, `DOCUMENT_OWNER`, `DOCUMENT_CORRESPONDENT`, `DOCUMENT_TAGS`, `DOCUMENT_ORIGINAL_FILENAME` and `TASK_ID`. It cannot cancel consumption and must not edit the document files.

## v3 breaking change
Positional arguments (`$1` to `$8`) are gone. Use the variables:
```bash
echo "Document ${DOCUMENT_ID} from ${DOCUMENT_CORRESPONDENT} tagged: ${DOCUMENT_TAGS}"
```

## Docker
Bind-mount the script directory and reference the in-container path:
```yaml
volumes:
  - /path/to/scripts:/path/in/container/scripts/
environment:
  PAPERLESS_POST_CONSUME_SCRIPT: /path/in/container/scripts/post.sh
```
Check permissions (`chmod 755`) and watch `docker compose logs -f`.

## Checked
2026-11-04. Compared with the pre and post consumption script sections of advanced_usage and the consume script section of the v3 migration page (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: both setting names, blocking behaviour and fork advice, pre-consume variables and the DOCUMENT_WORKING_PATH rule, duplicate warning, the pdf2pdfocr example, post-consume variables, inability to cancel, no file edits, removal of positional arguments $1 to $8, Docker mount example and troubleshooting tips. Nothing removed.

Method: documentation only; no commands were run.

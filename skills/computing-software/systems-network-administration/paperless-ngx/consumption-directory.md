---
id: computing-software.systems-network-administration.paperless-ngx.consumption-directory
name: consumption-directory
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, consumption-directory, consumer, subdirs-as-tags, ignore-patterns, scanner]
level: practitioner
status: docs-checked
description: "How the consume folder works: files are moved into storage, recursive watching, subfolders as tags, ignore patterns and the consumer disable switch."
sources:
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The consumption directory

Treat the folder as a temporary inbox. Consumed files are re-created in the media directory and removed from the consume folder, so do not use it as storage. Originals are never modified.

## Getting files there
Scanners usually push via FTP or SMB. Web UI upload, mail rules and the REST API are alternatives that skip the folder.

## Settings
- `PAPERLESS_CONSUMER_RECURSIVE=true` watches subdirectories. Workflow path filters can then assign owners by folder.
- `PAPERLESS_CONSUMER_SUBDIRS_AS_TAGS=true` turns folder names into tags (`foo/bar/file.pdf` gets `foo` and `bar`), creating missing tags. It requires recursive mode.
- `PAPERLESS_CONSUMER_IGNORE_PATTERNS`: JSON list of regexes matched against file names, added to the built-ins (`.DS_Store`, `._*`, `desktop.ini`, `Thumbs.db`). These are regular expressions, not globs: use `^\._.*`, not `._*`.
- `PAPERLESS_CONSUMER_IGNORE_DIRS`: extra directory names to skip; built-ins such as `.stfolder`, `@eaDir` and `__MACOSX` always apply.
- `PAPERLESS_CONSUMER_DISABLE`: if set, turns off the directory consumer in Docker.
- `PAPERLESS_FILENAME_DATE_ORDER` reads dates from file names that contain separators.

## Supported types
PDF and images (PNG, JPEG, TIFF, GIF, WebP) get OCR; plain text is added verbatim; Office types need Tika. Type is detected from content, but the consume folder rejects extensions no parser supports.

## Checked
2026-11-04. Compared with the consumption directory section of usage, the document consumption settings in configuration, and the supported file types entry of the FAQ (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: files re-created and removed from the folder, originals never overwritten, FTP/Samba scanner push, recursive and subdirs-as-tags behaviour, regex ignore patterns with the built-in lists, ignore dirs, consumer disable switch, filename date order, supported types and extension rejection. Nothing removed.

Method: documentation only; no commands were run.

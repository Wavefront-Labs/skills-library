---
id: computing-software.systems-network-administration.paperless-ngx.paths-and-folders
name: paths-and-folders
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, media-root, data-dir, consumption-dir, scratch-dir, paths]
level: practitioner
status: docs-checked
description: "Know what each Paperless-ngx directory setting holds and which ones to leave alone in Docker."
sources:
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/faq/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Paths and folders

| Setting | Holds | Default |
|---|---|---|
| `PAPERLESS_CONSUMPTION_DIR` | files to consume | `../consume/` relative to `src` |
| `PAPERLESS_DATA_DIR` | search index, SQLite DB, classification model, etc. | `../data/` relative to `src` |
| `PAPERLESS_MEDIA_ROOT` | documents and thumbnails | `../media/` relative to `src` |
| `PAPERLESS_SCRATCH_DIR` | temp workspace for consumption, editing, exporter | `/tmp/paperless` |
| `PAPERLESS_EMPTY_TRASH_DIR` | originals of deleted documents (e.g. after emptying the trash) | empty (really delete) |
| `PAPERLESS_LOGGING_DIR` | log files | `PAPERLESS_DATA_DIR/log/` |
| `PAPERLESS_MODEL_FILE` | classification model | `PAPERLESS_DATA_DIR/classification_model.pickle` |

## Rules of thumb
- In Docker do not change `PAPERLESS_CONSUMPTION_DIR`; it only changes the path within the container. Change the local consumption directory in `docker-compose.yml` instead.
- The trash directory must exist before you use the setting and be writeable by the user running Paperless. In Docker keep it inside a permanent volume (the docs give `../media/trash`) so upgrades do not lose it. Only the original version is kept. The setting was previously named `PAPERLESS_TRASH_DIR`.
- The model file uses Python pickle, so only the paperless user should be able to write it; a crafted model could execute code when loaded.
- Files consumed from the consumption folder are re-created inside the media directory and removed from the consumption folder.
- With Docker, the media volume is managed by Docker and Paperless; do not change its permissions or move files around manually.
- `PAPERLESS_MEDIA_ROOT` and `PAPERLESS_DATA_DIR` can be set to the same folder to keep all data in one volume.

Logs rotate at 1 MiB (`PAPERLESS_LOGROTATE_MAX_SIZE`, in bytes) keeping 20 rotated files (`PAPERLESS_LOGROTATE_MAX_BACKUPS`).

## Checked
Date: 2026-11-07
Pages read in full: configuration (docs/configuration.md), faq (docs/faq.md).
Corrections: reworded each default and rule to the page text; dropped "do not move files inside the media folder by hand" as a general rule and scoped it to the Docker media volume as the FAQ states; added the trash-dir previous name and shared-folder tip.
Method: documentation only; no commands were run.

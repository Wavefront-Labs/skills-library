---
id: computing-software.systems-network-administration.paperless-ngx.exporter-backup
name: exporter-backup
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, document-exporter, backup, export, rsync, passphrase]
level: practitioner
status: docs-checked
description: "Back up Paperless-ngx with document_exporter: incremental updates, zip output, filename options, passphrase encryption and version limits."
sources:
  - "https://docs.paperless-ngx.com/administration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporting and backing up

```bash
docker compose exec -T webserver document_exporter ../export
```
`-T` avoids "input device is not a TTY" errors in cron. In the provided compose files `../export` maps to the `export` folder on the host. The target receives originals, archives, thumbnails and `manifest.json` (all database metadata).

## Incremental behaviour
If the target already holds an export, only changed or new files are written, judged by modified time and size. `-c` compares checksums (slower). `-d` deletes files no longer part of the export; be careful pointing at a folder with other contents. This makes `rsync` style backups workable.

## Options
- `-f` uses `PAPERLESS_FILENAME_FORMAT` for names (watch path length limits).
- `-na` no archives, `-nt` no thumbnails. After import the sanity checker warns until they are regenerated.
- `-p` folders `archive`, `originals`, `thumbnails`, `json`; `-sm` one JSON per document.
- `-z` zip output, `-zn` name, `--zip-compression` (stored, deflated default, bzip2, lzma, zstd) and `--zip-compression-level`. zstd needs Python 3.14 on both export and import machines.
- `--data-only` exports just the database.
- `--no-progress-bar` for scripts.
- `--passphrase <PASSPHRASE>` encrypts some fields; lose it and the export cannot be imported.

## Limits
An export imports only into the same Paperless version, because it is an exact database image. API tokens are not exported.

Docker volume backups (`paperless_media`, `paperless_data`, `paperless_pgdata`, `paperless_dbdata`) are the other option. Before any backup, make sure Paperless is not actively consuming documents.

## Checked
2026-11-04. Compared with Making backups and Document exporter in administration (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: -T cron note, target contents, incremental behaviour, every option, zip compression choices and the zstd Python 3.14 warning, passphrase, same-version caution, API tokens not exported, the four volumes. Reworded the volume backup line to the docs' advice to make sure Paperless is not consuming.

Method: documentation only; no commands were run.

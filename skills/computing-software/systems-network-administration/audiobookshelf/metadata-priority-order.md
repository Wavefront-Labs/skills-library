---
id: computing-software.systems-network-administration.audiobookshelf.metadata-priority-order
name: metadata-priority-order
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [metadata, scanner, priority, metadata-json, opf, nfo]
level: advanced
status: docs-checked
description: "Set each library's local metadata order of precedence and know why the metadata.json source should stay on top."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/2.book-metadata.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scanning uses only local sources automatically; online matching is a manual action. Each library has its own "Metadata Order of Precedence". The server fills each database field from the **lowest** enabled priority first, then overwrites with the next, and so on, so fields are populated even when the top source lacks them.

All sources are enabled by default. Default order, highest first:

1. Audiobookshelf `metadata.json` (mirrors the database; stored under `/metadata/items` per item).
2. OPF file.
3. `desc.txt` and `reader.txt`.
4. NFO file.
5. File metadata (tags from audio or e-book files via ffmpeg).
6. Folder structure (lowest by default).

Keep `metadata.json` highest. If you disable it, edits made in Audiobookshelf are lost the next time the item is scanned or updated. Temporarily disable or lower it when you have changed another source (for example an OPF) and want that source to overwrite the database.

Calibre libraries: put OPF above folder structure so folder naming does not extract wrong information.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Book Metadata page (Local Metadata Priority Order).

Method: documentation only; no commands were run.

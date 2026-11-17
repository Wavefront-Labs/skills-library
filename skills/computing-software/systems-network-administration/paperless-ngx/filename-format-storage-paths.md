---
id: computing-software.systems-network-administration.paperless-ngx.filename-format-storage-paths
name: filename-format-storage-paths
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, filename-format, storage-paths, document-renamer, placeholders, jinja]
level: practitioner
status: docs-checked
description: "Control stored file names with PAPERLESS_FILENAME_FORMAT and storage paths, using Jinja placeholders and the document_renamer command."
sources:
  - "https://docs.paperless-ngx.com/advanced_usage/"
  - "https://docs.paperless-ngx.com/administration/"
  - "https://docs.paperless-ngx.com/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File name format and storage paths

By default files are stored as `0000123.pdf`. Set a template for folders and names; the extension is added for you.

```bash
PAPERLESS_FILENAME_FORMAT={{ created_year }}/{{ correspondent }}/{{ title }}
```

## Placeholders
`asn`, `correspondent`, `document_type`, `tag_list`, `title`, `created`, `created_year`, `created_year_short`, `created_month`, `created_month_name`, `created_day`, the matching `added_*` set, `owner_username`, `original_name` and `doc_pk`. A `document` object adds fields such as `checksum` and `page_count`.

## Behaviour
- Empty values print as "none"; `PAPERLESS_FILENAME_FORMAT_REMOVE_NONE=true` drops them and empty folders.
- Characters like `: \ /` become dashes. Collisions get `_01`, `_02`.
- A template error falls back to the default scheme. Over-long paths keep the old name and log an issue.
- Versioned files add `_v1`, `_v2` suffixes.
- `{{ custom_fields | get_cf_value('name', 'default') }}` reads custom fields.

## Storage paths
Each storage path is its own template. Documents are assigned one using the matching algorithms, and the assignment can be overwritten at any time:
```
Insurances = Insurances/{{ correspondent }}/{{ created_year }}-{{ created_month }}-{{ created_day }} {{ title }}
```
Documents without one use the global format. Editing or deleting a storage path moves files automatically.

## After changing the global format
Run `document_renamer` (no arguments) to move existing files; take a backup first. Never rename files in the media folder by hand, or Paperless reports them missing.

Setting a format with `../` can store files outside the media directory; inside Docker, files stored outside the predefined volumes are lost after a restart.

## Checked
2026-11-04. Compared with File name handling, Placeholders, Storage paths and Filename Templates in advanced usage, and Managing filenames in administration (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: default naming, example, placeholders, none handling and REMOVE_NONE, dash replacement, collision counters, fallback, path length behaviour, version suffix, get_cf_value, storage path example and global fallback, renamer behaviour, manual rename warning. Reworded the storage path assignment line and the ../ caution to match the docs.

Method: documentation only; no commands were run.

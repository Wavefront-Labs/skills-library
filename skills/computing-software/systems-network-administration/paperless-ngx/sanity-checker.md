---
id: computing-software.systems-network-administration.paperless-ngx.sanity-checker
name: sanity-checker
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, sanity-checker, document-sanity-checker, checksum, integrity, orphaned-files]
level: practitioner
status: docs-checked
description: "Run and schedule the Paperless-ngx sanity checker to detect missing, corrupt or inaccessible files and orphans."
sources:
  - "https://docs.paperless-ngx.com/administration/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/advanced_usage/"
  - "https://docs.paperless-ngx.com/faq/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sanity checker

```bash
document_sanity_checker
```
The command takes no arguments. Depending on the size of the archive it may take some time.

## What it detects
- Missing original, archive or thumbnail files.
- Originals, archives or thumbnails that are inaccessible due to improper permissions.
- Corrupted originals or archives, found by comparing their checksum against the one stored in the database.
- Documents without any content (warning).
- Orphaned files in the media directory (warning): files not referenced by any document.

## Schedule
`PAPERLESS_SANITY_TASK_CRON` is a crontab(5) expression; the default is `30 0 * * sun` (Sunday, 30 minutes past midnight). Set it to `disable` and the checker will not run automatically.

## Typical fixes
- Missing thumbnails: `document_thumbnails` (optionally `--document <id>`; `--processes` defaults to a quarter of the available processors).
- Missing archives: `document_archiver` (add `--overwrite` to regenerate existing ones, `--document <id>` for one document).
- Files moved or renamed by hand: Paperless remembers the last filename a document was stored as, so it reports such files as missing and cannot find them. Do not move files manually in the media folder.
- After exporting with `-na` or `-nt` and importing, the sanity checker warns about missing thumbnails and archive files until they are regenerated with `document_thumbnails` or `document_archiver`.

Paperless-ngx never modifies original documents; it keeps checksums of all documents and uses the scheduled sanity checker to check that they remain the same.

## Checked
Date: 2026-11-07
Pages read in full: administration, configuration, advanced_usage, faq (docs/*.md).
Removed as unconfirmed: "Results appear in the task list and logs"; the USERMAP_UID/GID permission fix (not tied to the sanity checker on these pages); "or rerun document_renamer" for hand-renamed files; "useful backup health check". Changed "-na or -nt export" wording to match the administration note.
Method: documentation only; no commands were run.

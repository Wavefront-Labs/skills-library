---
id: computing-software.database-administration.pgbackrest.file-bundling
name: file-bundling
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, bundling, repo-bundle, object-store, small-files]
level: advanced
status: docs-checked
description: "Combine small files into bundles to speed backups, especially on object stores, and know the downsides."
sources:
  - https://pgbackrest.org/user-guide.html
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reduce per-file overhead.

`repo-bundle=y` combines smaller files to reduce the total number written to the repository. Writing fewer files is generally more efficient, especially on object stores such as S3. Zero-length files are not stored except in the manifest. The user guide notes file creation time is relatively slow on S3, Azure and GCS, so bundling improves backup and restore performance there.

```
[global]
repo1-bundle=y
repo1-bundle-limit=2MiB
repo1-bundle-size=20MiB
```

- `repo-bundle-limit` (default 2MiB, range 8KiB to 1PiB): files larger than this are stored separately.
- `repo-bundle-size` (default 20MiB): target bundle size; uncompressed size can reach size plus limit. Do not set too high because retries redo the whole bundle.

Bundled files cannot be reused when a backup is resumed, so a higher limit means fewer resumable files. `repo-block` (block incremental) requires `repo-bundle` to be enabled first.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html). Removed: the 1000-file example and the list of bundling downsides, which the fetched pages do not state. 

Method: documentation only; no commands were run.

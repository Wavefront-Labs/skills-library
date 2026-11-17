---
id: computing-software.database-administration.pgbackrest.repository-types-and-path
name: repository-types-and-path
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, repo-type, repo-path, posix, cifs]
level: practitioner
status: docs-checked
description: "Choose repo-type (posix, cifs, s3, gcs, azure, sftp) and set repo-path with sizing advice."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick where backups and WAL live.

`repo-type` (default `posix`):

- `posix`: POSIX-compliant file system. If an NFS mount is used, the PostgreSQL rules for file systems when creating a cluster apply.
- `cifs`: like posix but disables links and directory fsyncs.
- `s3`: AWS Simple Storage Service.
- `gcs`: Google Cloud Storage.
- `azure`: Azure Blob Storage Service.
- `sftp`: Secure File Transfer Protocol.

`repo-path` (default /var/lib/pgbackrest) is where backups and archive are stored. The docs say space is hard to estimate in advance: take some backups, record the sizes of full, incr and diff backups, measure WAL generated per day, and extrapolate.

```
[global]
repo1-type=posix
repo1-path=/path/to/repo
```

Repository symlinks (`repo-symlink`, default y) create the latest and tablespace symlinks, mainly useful for snapshot-based in-place recovery; disable them on POSIX-like storage that does not support symlinks. All repository options are indexed (`repo1-`, `repo2-`); see the multiple-repository skill for combining them.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html). Nothing needed removing. 

Method: documentation only; no commands were run.

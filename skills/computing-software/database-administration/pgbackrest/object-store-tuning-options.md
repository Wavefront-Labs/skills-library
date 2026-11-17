---
id: computing-software.database-administration.pgbackrest.object-store-tuning-options
name: object-store-tuning-options
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, repo-storage, prefetch, upload-chunk-size, read-over]
level: advanced
status: docs-checked
description: "Options shared by object-store repositories: TLS verification, prefetch, read-over, upload chunk size and tags."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune S3, GCS and Azure repository behavior.

- `repo-storage-verify-tls` (default y): verify the storage certificate. `repo-storage-ca-file` and `repo-storage-ca-path` use a CA other than the system default.
- `repo-storage-host` and `repo-storage-port` (default 443) connect to a host or port other than the endpoint, typically for testing.
- `repo-storage-prefetch` (default 3, range 0 to 1024): requests to prefetch when reading from object stores. It is not true concurrency, only reduces request latency; open requests per read are prefetch plus one.
- `repo-storage-read-over` (default 64KiB, up to 1MiB): bundles may contain data not needed in restore, for example files that already exist; this skips over such data without starting a new read request, which is faster and for most storage classes cheaper.
- `repo-storage-upload-chunk-size`: larger chunks mean fewer requests but more memory, allocated per process, so a high `process-max` multiplies it. Defaults depend on type (S3 5MiB; GCS and Azure 4MiB). Valid sizes vary by store: part size for S3, chunk size for GCS, block size for Azure. Files over 1GiB get incrementally larger chunks.
- `repo-storage-tag`: tags added to objects; repeat for several. pgBackRest cannot modify them later, so set before `stanza-create`.

```
[global]
repo1-storage-prefetch=7
repo1-storage-read-over=128KiB
```

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html). Removed: the wording 'or a local store'. 

Method: documentation only; no commands were run.

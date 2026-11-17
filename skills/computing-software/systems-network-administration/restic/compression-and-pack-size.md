---
id: computing-software.systems-network-administration.restic.compression-and-pack-size
name: compression-and-pack-size
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, compression, pack-size, tuning, tmpdir, performance]
level: advanced
status: docs-checked
description: "Tune restic compression modes and pack size, and size temporary space for pack files with TMPDIR."
sources:
  - https://restic.readthedocs.io/en/stable/047_tuning_parameters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compression and pack size

## Compression

For a repository using at least repository format version 2, `--compression` sets how data is compressed. It applies
to the single run, or can be set with the `RESTIC_COMPRESSION` environment variable:

- `off`
- `fastest`
- `auto` (default)
- `better`
- `max`

Each setting uses more CPU but less bandwidth and storage space than the one before it in this list.

## Pack size

Restic defaults to a 16 MiB pack size. Change it with `--pack-size` or `RESTIC_PACK_SIZE` (integer MiB); specify it
for each restic command that modifies the repository.

- Larger packs reduce the number of files in the repository and help in very large (TiB range) repositories, with very
  fast upload connections, on backends with hard limits on file count (OpenStack Swift, some Google Drive Team
  accounts), and can improve backup speed for a repository on a local HDD.
- Restic needs temporary space of the pack size multiplied by the number of backend connections plus one. With 5
  connections (the default for most backends) and 64 MiB packs: a minimum of 384 MiB in the temp directory. Memory
  usage can also increase by a similar amount, depending on the backend.
- Larger packs take longer to upload, so they are more likely to be written to disk, which can increase SSD wear.

## Temporary directory

The space must be in the system default temp directory unless you set `TMPDIR` (on Windows, `TMP`):

```
TMPDIR=/path/to/scratch restic backup --pack-size 64 /path/to/data
```

## Checked
Compared with the "Tuning parameters" page: compression values, default and scope, 16 MiB default, `--pack-size` and
`RESTIC_PACK_SIZE`, temp space formula and 384 MiB example, SSD wear and the `TMPDIR`/`TMP` variables. Removed: advice
on when to pick `max`, `fastest` or `off`, the "high-latency backends" benefit for larger packs and the
change-one-setting-at-a-time tip (not on the page).
Method: docs-only read of cited pages, 2026-11-08

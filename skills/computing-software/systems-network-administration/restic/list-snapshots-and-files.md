---
id: computing-software.systems-network-administration.restic.list-snapshots-and-files
name: list-snapshots-and-files
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, snapshots, ls, ncdu, listing, json]
level: intro
status: docs-checked
description: "List snapshots with restic snapshots and browse their contents with restic ls, including sorting, long output, JSON and ncdu export."
sources:
  - https://restic.readthedocs.io/en/stable/045_working_with_repos.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Listing snapshots and files

## Snapshots

```
restic -r /srv/restic-repo snapshots
restic snapshots --host myhost --path /path/to/data
restic snapshots --group-by host
```

`--host` and `--path` filter (filters can be combined); `--group-by` groups the output by host, paths or tags.

## Files inside a snapshot

```
restic ls latest
restic ls <snapshotID> --long
restic ls latest --recursive --host myhost
```

- `--recursive` also lists subdirectories of the directories you name.
- `--long` shows file permissions, UID, GID, size, modification time and path.
- `--json` gives machine-readable output.
- `--sort name|size|time=mtime|atime|ctime|extension` and `--reverse` change order; the default is `name`. Sorting
  works with `--json` and without `--long`, but is mutually exclusive with `--ncdu`.
- `--ncdu` writes NCDU-format output so you can explore disk usage:

```
restic ls latest --ncdu | ncdu -f -
```

Positional arguments after the snapshot ID are absolute directory paths (forward slashes); only files inside those
directories are listed, and files in subdirectories only with `--recursive`, e.g. `restic ls latest /home`.

## Choosing the right snapshot

The special ID `latest` lists the latest snapshot in the repository, and `--host` selects the latest from one host.
When several hosts share a repository, add `--host` to avoid picking another machine's snapshot.

Pair `ls` with `restic find` when you know a file name but not the snapshot.

## Checked
Compared with the "Working with repositories" page: `snapshots` filters (`--path`, `--host`, `--group-by`), `ls`
with `latest`, directory arguments, `--recursive`, `--long` columns, `--json`, `--sort` values and default,
`--reverse` and `--ncdu`. Corrected the `--long` description. Removed: `--path` with `latest` and `restic diff` (not
on the page).
Method: docs-only read of cited pages, 2026-11-08

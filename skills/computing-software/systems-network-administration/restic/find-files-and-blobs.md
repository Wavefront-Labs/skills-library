---
id: computing-software.systems-network-administration.restic.find-files-and-blobs
name: find-files-and-blobs
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, find, search, blob, snapshots, newest, oldest]
level: practitioner
status: docs-checked
description: "Locate files, directories and blobs across restic snapshots with restic find, its host, path and tag filters, and file modification-time limits."
sources:
  - https://restic.readthedocs.io/en/stable/045_working_with_repos.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding things

## Files and directories

```
restic find 'report*.pdf'
restic find --snapshot latest '*.conf'
restic find --host myhost --path /path/to/data --newest '2026-01-01' notes.txt
```

`find` searches for files or directories stored in the repository. All positional parameters are patterns (the
exclude-pattern syntax); quote names with spaces, such as "file one.bar", and if in doubt use a quoted wildcard like
"*.txt". Filters:

- `--snapshot` (repeatable) limits the search to given snapshots; without it `find` searches all snapshots
- `--host`, `--path` and `--tag` are the standard filter options
- `--oldest` and `--newest` select files whose inode modification time is in the interval (not the snapshot time);
  giving only one is a valid half-open interval, e.g. `--oldest 2025-01-01 --newest "2025-12-31 23:59:59" "*.txt"`
- `--json` output works for these commands

## Blobs, trees and packfiles

```
restic find --blob <blobID>
```

The other find options are devoted to finding blobs, trees and packfiles. They are typically not used by normal
users but can help debug a problem with restic. The example output names the file, tree and snapshot that contain
the blob.

## Related tools

- `restic ls` lists the contents of one snapshot.

## Checked
Compared with the "Working with repositories" page: find patterns and quoting, `--snapshot`, standard filters,
`--oldest`/`--newest` semantics, `--json` and the `--blob` example. Corrected: `--oldest`/`--newest` apply to file
modification time, not snapshot time. Removed: the `--tree` and `--pack` flag names, the `restore --include` tip, the
Match and Blob JSON object names, and the `cat`, `list` and `repair snapshots` entries (not on the page).
Method: docs-only read of cited pages, 2026-11-08

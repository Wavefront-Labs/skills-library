---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.path-specific-filer-store
name: path-specific-filer-store
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [location, per-path-store, filer-toml, path-specific]
level: advanced
status: docs-checked
description: "Route a directory subtree to its own filer store with a named section such as [redis2.tmp] and location, to isolate hot paths or scale metadata."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Path-Specific-Filer-Store
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# path specific filer store

Use when one store cannot cope: critical data needing strong consistency, a directory with heavy churn, total entries beyond one store, or one hot directory to isolate.

Run `weed scaffold -config=filer` and follow its notes:
1. Name the section as the store type plus a dot and a label, e.g. `[redis2.tmp]`.
2. Add `location = "/tmp/"`.
3. Copy and customize the other settings (they must differ from the other store of the same type).
4. Set `enabled = true`.

```toml
[redis2.tmp]
enabled = true
location = "/tmp/"
address = "localhost:6379"
password = ""
database = 0
```
You can add many; matching a request path to locations is efficient and unlimited in count.

Gotchas:
- Only new data and updates go to the new store. Existing entries under that path become invisible, so apply it to new directories only.
- The `location` prefix is trimmed before persisting: with `location = "/team/"`, the file `/team/tmp/file.txt` is stored as `/tmp/file.txt` (same pattern as the page's example) and the prefix is added back on read. This makes the store portable: `location` can later change to another directory or even another filer.

What still works: renames across filer stores, metadata export and import, and cross-cluster replication.

How it works: each request's directory is matched against all configured locations, and the matched store handles the metadata reads and writes.

## Checked

2026-11-08. Confirmed against the Path-Specific Filer Store wiki page. Removed the unsupported "write a file and check the key" verification and corrected the trimming example; added the portability, what-still-works and matching notes.

Method: documentation only; no commands were run.

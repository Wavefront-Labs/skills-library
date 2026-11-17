---
id: computing-software.systems-network-administration.ceph.rbd-live-migration
name: rbd-live-migration
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, rbd, live-migration, prepare, execute, commit]
level: sme
status: docs-checked
description: "Move an RBD image between pools or import external data with rbd migration prepare, execute and commit."
sources:
  - https://docs.ceph.com/en/latest/rbd/rbd-live-migration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Live migration has three steps, with an abort path. It needs the Nautilus release or later (external data sources need Pacific or later), and the `krbd` kernel module does not support it.

```
rbd migration prepare migration_source [migration_target]
rbd migration execute migration_target
rbd migration commit migration_target
```

- `prepare` creates the target image and links it to the source. Outside import-only mode the source is also linked to the target and marked read-only, and moved to the RBD trash (`rbd trash ls --all` shows it). Reads of uninitialized extents in the target redirect to the source, and writes to uninitialized extents deep-copy the overlapping source block.
- `execute` deep-copies all initialized blocks from the source to the target in the background; clients may use the target meanwhile.
- `commit` removes the cross-links between source and target and, outside import-only mode, removes the source image. If the source is a parent of clones, `--force` is needed after ensuring all descendent clones are not in use.

Revert before commit:

```
rbd migration abort migration_target
```

Abort removes the cross-links and deletes the target, restoring access to the source.

Import-only migration from an external source described in JSON:

```
rbd migration prepare --import-only --source-spec "<JSON>" migration_target
```

The source-spec can also come from a file or STDIN with `--source-spec-path`. Supported formats are `native`, `qcow` and `raw`; supported streams are `file`, `http`, `s3` and `nbd`. In import-only mode the source image stays unmodified.

`prepare` accepts the same layout options as `rbd create`, so the immutable on-disk layout can change; `migration_target` may be skipped if the goal is only a layout change keeping the original name.

All clients of the source must be stopped before `prepare` (outside import-only mode); it fails if any client has the image open read/write. Afterwards restart clients using the target name; restarting with the source name fails. `rbd status migration_target` shows the migration state (for example `prepared`, `executing (32% complete)`, `executed`).

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against "Image Live-Migration" on docs.ceph.com. Corrected the prepare description (reads of uninitialized extents go to the source; writes there deep-copy) and removed the unsupported statement that writes go to the target while reads fall back wholesale.

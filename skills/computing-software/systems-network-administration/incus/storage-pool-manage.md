---
id: computing-software.systems-network-administration.incus.storage-pool-manage
name: storage-pool-manage
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, storage, storage-pool, set, edit, info, resize, loop-backed]
level: practitioner
status: docs-checked
description: "Inspect and change Incus storage pools: list, show, info, set, edit and resize (loop-backed pools can grow but not shrink)."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/storage_pools.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manage storage pools

```
incus storage list
incus storage show <pool>
incus storage info <pool>
incus storage set my-dir-pool rsync.compression=false
incus storage edit <pool>
incus storage set <pool> size=<new_size>
```

- `show` gives configuration; `info` gives usage.
- General keys such as `source` are top-level; driver-specific keys carry the driver name as prefix.
- Resize works only for loop-backed pools managed by Incus, and only to grow.
- Pool-wide volume defaults use the `volume.<key>` prefix (see storage-volume-config-resize).

## Checked

2026-11-04: confirmed against the Incus storage pools and storage volumes how-tos (list/show/info/set/edit, top-level versus driver-prefixed keys, resize limited to growing loop-backed pools, `volume.` defaults). Nothing removed.

Method: documentation only; no commands were run.

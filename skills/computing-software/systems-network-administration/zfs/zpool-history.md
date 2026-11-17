---
id: computing-software.systems-network-administration.zfs.zpool-history
name: zpool-history
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, history, audit, long-format, internal-events]
level: intro
status: docs-checked
description: "Review the commands run against ZFS pools with zpool history, adding internal events with -i and user, host and zone details with -l."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-history.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool history

```
zpool history [-il] [pool]...
```

Shows the command history of the named pools, or of all pools if none is given.

```
zpool history tank
zpool history -l tank
zpool history -i tank
zpool history -il tank
```

## Options

- `-i`: also display internally logged ZFS events, in addition to user-initiated events.
- `-l`: long format; adds the user name, hostname and zone in which each operation was performed.

See also zpool-events and zpool-status-health. The man page documents only these two options.

## Checked

2026-11-03. Pages read: zpool-history(8).

Confirmed: synopsis, default of all pools, -i and -l meanings.

Removed or corrected: the use-case bullets and the claim that history moves with an exported pool, which the page does not state.

Method: documentation only; no commands were run.

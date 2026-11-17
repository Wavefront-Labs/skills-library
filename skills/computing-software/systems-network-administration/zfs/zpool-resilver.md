---
id: computing-software.systems-network-administration.zfs.zpool-resilver
name: zpool-resilver
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, resilver, restart, deferred-resilver, progress]
level: practitioner
status: docs-checked
description: "Start or restart a ZFS resilver with zpool resilver: the discard-and-restart behaviour, deferred resilvers, and progress above 100 percent."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-resilver.8.html
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-wait.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool resilver

```
zpool resilver pool...
```

Starts a resilver on each named pool. Resilvering follows attaching or replacing a device (see zpool-attach-mirror and zpool-replace-device); this command starts one explicitly.

```
zpool resilver tank
zpool status tank
zpool wait -t resilver tank
```

## Behaviour

- If a resilver is already running, it is restarted from the beginning.
- Drives waiting in the deferred-resilver queue are included in the new resilver.
- Deferred resilvers require the `resilver_defer` pool feature.
- On a live pool, writes can make the reported progress exceed 100% completion.

## Related behaviour from other pages

- A scrub cannot start during a resilver, and only one runs per pool at a time (see zpool-scrub).
- `zpool attach` and `zpool replace` cancel a running scrub and start a resilver (see zpool-attach-mirror and zpool-replace-device).
- Sequential reconstruction (`-s` on attach or replace) restores redundancy faster but skips checksum verification, so a scrub follows.

Wait for completion in scripts with `zpool wait -t resilver`. See zpool-wait.

## Checked

2026-11-03. Pages read: zpool-resilver(8), zpool-scrub(8), zpool-attach(8), zpool-replace(8), zpool-wait(8).

Confirmed: synopsis, restart behaviour, deferred resilvers and the resilver_defer feature, progress above 100%, scrub and resilver exclusivity, scrub cancellation on attach and replace, -s behaviour.

Removed or corrected: the claim that online starts a resilver and the do-not-run-casually advice.

Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.zfs.zpool-wait
name: zpool-wait
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, wait, scripting, activity, progress]
level: practitioner
status: docs-checked
description: "Block until ZFS background activity finishes with zpool wait: activity names, -t selection, interval progress output, and scripting flags -H, -p, -T."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-wait.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool wait

```
zpool wait [-Hp] [-T u|d] [-t activity[,activity]...] pool [interval]
```

Waits until background activity of the given types stops in the pool. Activity can stop by completing, being paused or cancelled by a user, or the pool being exported or destroyed. With no `-t` list it waits for every activity type. If nothing of the given types is running, it returns immediately.

```
zpool wait -t scrub tank
zpool wait -t resilver,replace tank 10
```

If `interval` is given, the remaining work for each activity, in bytes, is printed every `interval` seconds.

## Activities for -t

- `discard`: a checkpoint to be discarded
- `free`: the `freeing` property to reach 0
- `initialize`: all initializations to stop
- `replace`: all device replacements to stop
- `remove`: device removal to stop
- `resilver`: resilver to stop
- `scrub`: scrub to stop
- `trim`: manual trim to stop
- `raidz_expand`: attaching to a RAID-Z vdev to complete
- `condense`: metadata condense operations to complete

## Output flags

- `-H`: scripted; no headers, tab-separated.
- `-p`: exact parsable numbers.
- `-T u|d`: timestamp, internal representation or standard date format.

Many other subcommands also accept `-w` to wait for their own operation; use `zpool wait` when the operation was started earlier or by something else.

## Checked

2026-11-03. Pages read: zpool-wait(8).

Confirmed: synopsis, semantics, every activity name, interval output, -H, -p, -T.

Removed or corrected: the invented activity alias freeing.

Method: documentation only; no commands were run.

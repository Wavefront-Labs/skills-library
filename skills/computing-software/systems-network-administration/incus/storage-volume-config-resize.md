---
id: computing-software.systems-network-administration.incus.storage-volume-config-resize
name: storage-volume-config-resize
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, storage-volume, volume-set, resize, volume-list, backups-volume, images-volume]
level: practitioner
status: docs-checked
description: "View, configure and resize Incus storage volumes: volume.<key> pool defaults, volume_type prefixes, grow/shrink rules, and storage.backups_volume / storage.images_volume."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/storage_volumes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volume configuration and resize

```
incus storage volume list <pool> [--all-projects]
incus storage volume show <pool> [<type>/]<volume>
incus storage volume info <pool> [<type>/]<volume>
incus storage volume set <pool> [<type>/]<volume> size=1GiB
incus storage volume edit <pool> [<type>/]<volume>
incus config set storage.backups_volume=<pool>/<volume>
incus config set storage.images_volume=<pool>/<volume>
```

- Default type is `custom`; instance volumes need `container/c1` style names to avoid clashes.
- Pool defaults: `incus storage set <pool> volume.<key>=<value>`. Volume settings override pool defaults; instance settings override volume settings.
- Resize custom volumes with `size=`; VM root disks with `incus config device set my-vm root size=<new_size>`.
- Growing usually works if the pool has space. Shrinking works only for filesystem volumes, is not guaranteed, and cannot go below used size. Block volumes cannot shrink.
- Disk I/O limits: `limits.read`, `limits.write`, `limits.max` (bytes/s or `iops`). VMs also take `limits.<type>.burst` and `.burst.length`.

## Checked

2026-11-04: confirmed against the Incus storage volumes how-to (list/show/info/set/edit, default `custom` type, pool defaults and override order, resize rules, I/O limits and burst properties, backups/images volume settings). Nothing removed.

Method: documentation only; no commands were run.

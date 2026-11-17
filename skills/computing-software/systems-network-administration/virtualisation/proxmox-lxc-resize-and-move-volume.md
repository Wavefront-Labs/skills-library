---
id: computing-software.systems-network-administration.virtualisation.proxmox-lxc-resize-and-move-volume
name: proxmox-lxc-resize-and-move-volume
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pct-resize, pct, lxc, pct-move-volume, rootfs, proxmox]
level: practitioner
status: docs-checked
description: "Grow Proxmox container root and mount point volumes with pct resize, shrink them via backup/restore, and move volumes between storages."
sources:
  - https://pve.proxmox.com/pve-docs/pct.1.html
  - https://github.com/proxmox/pve-docs/blob/master/pct.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resizing and moving container volumes

## Grow
```sh
pct resize 201 rootfs +10G       # relative
pct resize 201 mp0 200G          # absolute
pct exec 201 -- df -h /
```
A `+` prefix adds to the current size; without it the value is absolute. Shrinking a volume is not supported by `pct resize`.

## Shrink (restore into a smaller volume)
1. Back up: `vzdump 201 --storage pbs01 --mode stop`.
2. Restore with a smaller rootfs:
   ```sh
   pct restore 201 pbs01:backup/ct/201/<backup-time> --rootfs local-lvm:8 --force
   ```
   Setting `--rootfs` switches `pct restore` to advanced mode, which ignores the rootfs and mpX entries from the archive and uses the given parameters (`<storage>:<size in GiB>`); the data must fit in the new size.

## Move to another storage
```sh
pct move-volume 201 rootfs ceph-ct --delete 1     # without --delete the original stays as an unused volume entry
pct move-volume 201 mp0 local-zfs
```

## Gotchas
- If the size in the config no longer matches the volume, `pct rescan` rescans all storages and updates disk sizes and unused disk images (`--dryrun 1` to preview).
- Mount points with `backup=0` are not in vzdump: shrinking via restore loses their data
  unless copied separately.
- Bind mounts (`mp0: /mnt/data,mp=/data`) are host paths, not volumes: resize/move do not
  apply.

## Verify
`pct config 201` size matches `df -h` inside; services healthy after resize or restore.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: generated pct.1-synopsis.adoc resize, move-volume, rescan and restore entries; pct.adoc restore section) and confirmed that shrinking is not supported, the + sign semantics, --delete behaviour and the pct rescan options. Removed the unconfirmed ZFS refquota shrink, filesystem-resize detail, GUI path and stop-required claims.

Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.proxmox-ve.zfs-arc-limit-and-zed-mail
name: zfs-arc-limit-and-zed-mail
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [zfs-arc-max, arc, zed, zfs-conf, modprobe]
level: advanced
status: docs-checked
description: "Limit the ZFS ARC size and configure ZED email alerts on a Proxmox VE host."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default ZFS uses 10% of host memory, capped at 16 GiB, for the ARC; the installer writes this to `/etc/modprobe.d/zfs.conf`. Installs that predate Proxmox VE 8.1 kept ZFS's own default (50%, or 62.5% on ZFS 2.3.0 or newer) unless changed manually. Reduce it with care since ARC size drives IO performance. Rule of thumb: 2 GiB base plus 1 GiB per TiB of storage, so an 8 TiB pool gets 10 GiB. ZFS enforces a minimum of 64 MiB.

Change for the current boot only:

```
echo "$[10 * 1024*1024*1024]" >/sys/module/zfs/parameters/zfs_arc_max
```

Make it permanent in `/etc/modprobe.d/zfs.conf`:

```
options zfs zfs_arc_max=8589934592
```

If the value is not above `zfs_arc_min` (default 1/32 of system memory, relevant on hosts with more than 256 GiB), it is ignored unless you also set `zfs_arc_min` to at most `zfs_arc_max - 1`. When root is on ZFS run `update-initramfs -u -k all`, then reboot.

ZED, the ZFS event daemon (package `zfs-zed`, installed by default), emails about pool events. Configure `/etc/zfs/zed.d/zed.rc`; the key setting is `ZED_EMAIL_ADDR`, default `"root"`. Mail to root is forwarded to the root user's configured address.

Swap on a zvol can block the server or cause high IO, for example when starting backups to external storage. Prefer a swap partition on a physical disk, plenty of RAM, and `vm.swappiness = 10` in `/etc/sysctl.d/99-swappiness.conf` (default is 60).

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-sysadmin.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.

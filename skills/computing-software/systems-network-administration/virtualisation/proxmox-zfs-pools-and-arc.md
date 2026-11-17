---
id: computing-software.systems-network-administration.virtualisation.proxmox-zfs-pools-and-arc
name: proxmox-zfs-pools-and-arc
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-zfs, zfs-arc, zfs, zpool, zfs-replace, volblocksize, zfs-scrub, pve-storage, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Run ZFS on Proxmox VE: pool layout for VMs (mirrors vs RAIDZ), ARC memory cap, volblocksize, scrubs, replacing a failed (boot) disk with proxmox-boot-tool."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#chapter_zfs
  - https://github.com/proxmox/pve-docs/blob/master/local-zfs.adoc
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-zfspool.adoc
  - https://openzfs.github.io/openzfs-docs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ZFS on Proxmox VE

**Goal:** ZFS pools that give VMs good IOPS, leave memory for guests, and survive disk
failures with a tested replacement procedure.

## Layout
- **Mirrors (RAID1) and striped mirrors (RAID10)** have favourable behaviour for VM workloads; a RAIDZ vdev behaves like roughly a single disk for IOPS. In a mirror vdev at least one healthy disk per mirror is needed. RAIDZ-1/2/3 need at least 3/4/5 disks. For a 4-disk RAIDZ2 the guide suggests two mirror vdevs instead (same usable space, better performance).
- `ashift` should match or exceed the disk's sector size (`zpool create -f -o ashift=12 <pool> ...` in the guide); it cannot be changed later, and `ashift=9` can perform badly.
- Use fast SSDs with power-loss protection for log (SLOG) and cache devices.
- Do not use ZFS on top of a hardware RAID controller with its own cache; use an HBA or an LSI controller in IT mode.

## ARC memory
By default PVE sets the ARC limit to 10% of host memory, clamped to a maximum of 16 GiB, and writes it to `/etc/modprobe.d/zfs.conf` at installation. Before PVE 8.1 no limit was set, so ZFS's own default applied (50%, or 62.5% from ZFS 2.3.0). The guide's rule of thumb is at least 2 GiB base plus 1 GiB per TiB of storage for the ARC. Change the limit permanently with a modprobe option and, when the root file system is ZFS, update the initramfs and reboot:
```sh
echo "options zfs zfs_arc_max=8589934592" > /etc/modprobe.d/zfs.conf    # 8 GiB
update-initramfs -u -k all
echo "$[10 * 1024*1024*1024]" >/sys/module/zfs/parameters/zfs_arc_max   # current boot only
```
If the desired `zfs_arc_max` is lower than or equal to `zfs_arc_min` (default 1/32 of system memory), it is ignored unless you also set `zfs_arc_min` to at most `zfs_arc_max - 1`.

## VM disks
VM disks are zvols. The `blocksize` storage property sets the default volblocksize for new zvols and applies only when a zvol is created; the guide gives 8k as the default ZVOL block size. On RAIDZ a small volblocksize wastes space on parity (each 8k block on a RAIDZ2 with ashift=12 needs two extra 4k parity blocks), so raise `volblocksize` or use mirrors. Enable `discard` on the VM disk so a TRIM-capable guest frees space.

## Health
```sh
zpool status -v             # shows resilver progress and errors
zpool list
```
The `zpool status` and `zpool list` commands are the standard ZFS tools; consult the OpenZFS documentation for scrub scheduling and capacity guidance, which are not covered by the Proxmox guide.

## Replace a failed disk (boot pool example)
```sh
proxmox-boot-tool status                              # systemd-boot/GRUB via proxmox-boot-tool, or plain GRUB
sgdisk <healthy bootable device> -R <new device>
sgdisk -G <new device>
zpool replace -f <pool> <old zfs partition> <new zfs partition>
proxmox-boot-tool format <new disk's ESP>
proxmox-boot-tool init <new disk's ESP> [grub]
```
The last two commands apply when the system boots through `proxmox-boot-tool`; plain GRUB systems need different steps (see the guide). For data pools: `zpool replace -f <pool> <old-device> <new-device>` and watch the resilver with `zpool status -v`.

## Verify
`zpool status` shows ONLINE, resilver complete, no errors; `proxmox-boot-tool status` lists
both boot partitions; ARC max matches the intended cap.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09).

Confirmed in the ZFS chapter: default ARC limit (10% of RAM, max 16 GiB, installer writes `/etc/modprobe.d/zfs.conf`; 50% or 62.5% before 8.1), the 2 GiB + 1 GiB/TiB rule, the runtime and permanent `zfs_arc_max` methods, `update-initramfs -u -k all` and reboot when root is on ZFS, the `zfs_arc_min` caveat; RAID level disk minimums, mirror versus RAIDZ behaviour, ashift guidance, HBA/IT-mode requirement, power-loss-protected SSDs; the default ZVOL block size (8k, not 16k as the draft said) and that `volblocksize` is set at creation; the failed-device replacement and `proxmox-boot-tool format/init` steps. Removed as unconfirmed: the "monthly scrub by default" claim, the 80% fill rule, `arc_summary`, the `by-id` naming rule and the old "16k in PVE 8+" figure.

Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.virtualisation.proxmox-iso-installer-zfs-and-disk-options
name: proxmox-iso-installer-zfs-and-disk-options
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-iso-installer, proxmox, zfs, lvm, installation]
level: practitioner
status: docs-checked
description: "Install Proxmox VE from the ISO choosing the right filesystem (ext4/xfs LVM, ZFS RAID, BTRFS) and advanced disk options like hdsize, ashift, swapsize and maxvz."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#installation_installer
  - https://pve.proxmox.com/wiki/ZFS_on_Linux
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox VE ISO installer: filesystem and disk options

**Goal:** a host installed with a boot layout that fits its hardware and storage plan.

## Choosing the target filesystem
| Option | Use when |
|---|---|
| ext4 or xfs (on LVM, with LVM-thin `local-lvm`) | Single disk or hardware RAID controller |
| ZFS RAID0/1/10/RAIDZ1-3 | HBA/IT-mode disks; want snapshots, replication, checksums |
| BTRFS RAID0/1/10 | Technology preview in the admin guide |

Never put ZFS on top of a hardware RAID volume; set the controller to HBA/passthrough mode.

## Advanced options (button next to target disk)
**LVM (ext4/xfs)**
- `hdsize`: total disk space to use (leave the rest unpartitioned).
- `swapsize`: defaults to the installed memory, clamped between 4 GiB and 8 GiB; 0 creates no swap volume.
- `maxroot`: maximum size of the root volume.
- `minfree`: free space left in the VG (for LVM snapshots).
- `maxvz`: maximum size of the data volume.

**ZFS**
- `ashift`: pool sector size exponent; it must be at least the sector size of the disks.
- `ARC max size`: the installer proposes a limit (recent releases default to 10% of RAM, capped at 16 GiB); adjust for hosts with lots of guests.
- `hdsize`: leave space unpartitioned, for example for an SSD over-provisioning reserve.

## Other installer screens
- Country/timezone/keyboard; root password and email (receives notifications).
- Management interface, FQDN, IP, gateway, DNS. The FQDN must resolve to that IP; it lands in `/etc/hosts`.
- Graphical, terminal UI, or terminal UI with serial console install modes; *Debug mode* drops to shells for troubleshooting.

## After install
- `zpool status` / `lvs` to confirm layout; `proxmox-boot-tool status` to see ESPs on ZFS installs.
- Switch repositories (enterprise vs no-subscription) before updating.

## Gotchas
- Unattended installs use an answer file instead of these screens.

## Checked

2026-10-28

Confirmed: Admin guide installation chapter and Automated Installation wiki: hdsize, swapsize default and clamp, maxroot, maxvz, minfree, ARC default (10% of RAM, max 16 GiB), BTRFS technology preview, Debug and serial console modes, proxmox-boot-tool status.

Removed or corrected: pve/root name, local-lvm claim, ashift immutability, compress/checksum line, mismatched-disk and stale-label gotchas, console=ttyS0.

Method: documentation only; no commands were run.

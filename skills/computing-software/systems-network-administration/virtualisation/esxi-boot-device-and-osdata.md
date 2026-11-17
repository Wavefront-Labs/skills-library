---
id: computing-software.systems-network-administration.virtualisation.esxi-boot-device-and-osdata
name: esxi-boot-device-and-osdata
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-boot-device, osdata, esxi-installation, systemmediasize, sd-card, usb-boot, boot-from-san, scratch-partition, coredump, vmware, esxi, vsphere]
level: practitioner
status: docs-checked
description: "Choose and size ESXi 7/8 boot media: OSDATA layout, systemMediaSize, why SD/USB boot is deprecated, relocating scratch/coredump, and migrating off SD cards."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=85685
  - https://knowledge.broadcom.com/external/article?legacyId=81166
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esxi-installation-and-setup-8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESXi boot device and OSDATA sizing

**Goal:** boot media that will not wear out or fill up, and a layout that survives
upgrades.

## ESXi 7/8 partition layout
| Partition | Contents |
|---|---|
| System boot | bootloader |
| Boot banks 0/1 | the running and fallback image |
| ESX-OSData | scratch, logs, VMware Tools images, coredump, trace; replaces the old scratch/locker partitions |
| VMFS datastore | whatever space remains (if the device is large) |

OSDATA is sized from the device unless overridden at install time with the boot option
`systemMediaSize=min|small|default|max` (with ESXi 7.0 U1c the default system storage is
138 GB; see KB 81166 for the per-option sizes). On a large boot disk use `small` or `min`
if you want the rest as datastore.

## Media choice
- Recommended: a **mirrored pair of M.2/BOSS SSDs** or local SAS/SATA SSD; 128 GB minimum
  for 9.x per KB 85685.
- **SD cards and USB sticks** are not recommended: reliability and write-endurance problems
  hit the OSDATA partition (KB 85685). Broadcom supports them as a boot device through the
  VCF 9.0 release and plans to move away from them; vSphere 8.0 install/upgrade workflows
  relocate OSDATA to a persistent device. If booting from SD, plan a separate persistent
  device for OSDATA.
- Boot from SAN works but makes the host depend on fabric zoning; keep one LUN per host
  and mask it from all others.

## Relocating scratch and coredump (legacy or SD hosts)
```sh
esxcli system coredump file add -d <datastore> -f <hostname>-dump
esxcli system coredump file set --smart --enable true
```
Logs can also be relocated to a datastore with `esxcli system syslog config set --logdir`
(KB 2003322).

## Migrating off SD cards
Fit the new boot device, back up the host configuration, fresh-install the same build to
the new device, then restore the configuration backup (host in maintenance mode, same
build number), and remove the SD card from the boot order.

## Verify
Check for an OSDATA volume on persistent storage, an active coredump target, and no
bootbank alarms.

## Checked
2026-10-31: OSDATA purpose and SD/USB guidance (support through VCF 9.0, 8.0 workflows relocating OSDATA, 128 GB minimum for 9.x, persistent-device recommendation) confirmed in KB 85685; the `systemMediaSize` boot option and 138 GB default confirmed in KB 81166; `esxcli system coredump file add/set` and syslog `--logdir` confirmed in KB 2003322/2004299. Removed unconfirmed figures: partition sizes (~100 MB/~500 MB/25 GB/32 GB), the ScratchConfig advanced-setting command, the vim-cmd firmware backup/restore commands and the bootbank error string.
Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.linux.kickstart-storage-partitioning
name: kickstart-storage-partitioning
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kickstart, ks-partitioning, autopart, clearpart, logvol, ignoredisk, anaconda, reqpart]
level: advanced
status: docs-checked
description: "Define disk layouts in kickstart: ignoredisk/clearpart safety, autopart vs part/volgroup/logvol, reqpart for EFI/biosboot, RAID and LUKS, and %pre-generated layouts."
sources:
  - https://pykickstart.readthedocs.io/en/latest/kickstart-docs.html
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/automatically_installing_rhel/kickstart-commands-and-options-reference_rhel-installer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kickstart storage and partitioning

## Safety first
```
ignoredisk --only-use=nvme0n1          # never touch other disks (SAN LUNs, data disks)
clearpart --all --initlabel --drives=nvme0n1
zerombr
```
Without `--only-use`, a kickstart can wipe attached SAN volumes. Prefer stable names:
`--only-use=disk/by-path/pci-0000:00:17.0-ata-1` or `disk/by-id/...`.

## Automatic
```
autopart --type=lvm --nohome --fstype=xfs     # --encrypted --passphrase=... ; types: lvm, btrfs, plain (alias partition), thinp, stratis
```
## Explicit layout (CIS-style separate partitions)
```
reqpart --add-boot                       # creates EFI system partition / biosboot as the firmware requires, plus /boot
part pv.01 --size=1 --grow --ondisk=nvme0n1
volgroup vg_sys pv.01
logvol /        --vgname=vg_sys --name=root --size=20480 --fstype=xfs
logvol /var     --vgname=vg_sys --name=var  --size=20480 --fstype=xfs
logvol /var/log --vgname=vg_sys --name=log  --size=8192  --fstype=xfs
logvol /tmp     --vgname=vg_sys --name=tmp  --size=4096  --fsoptions="nodev,nosuid,noexec"
logvol swap     --vgname=vg_sys --name=swap --recommended
logvol /home    --vgname=vg_sys --name=home --size=1 --grow --fsoptions="nodev"
```
Sizes are in MiB, with no unit suffix. `reqpart --add-boot` creates the platform partition (`/boot/efi` on UEFI x86_64 and Aarch64, `biosboot` on BIOS with GPT) plus a separate `/boot`, and cannot be combined with `autopart`. Leave free space in the VG (don't `--grow` everything) for snapshots and later growth.

## RAID and encryption
```
part raid.11 --size=1 --grow --ondisk=sda
part raid.12 --size=1 --grow --ondisk=sdb
raid pv.01 --level=1 --device=md0 raid.11 raid.12
part pv.02 --size=1 --grow --encrypted --luks-version=luks2 --passphrase=CHANGE_ME
```

## Dynamic layouts
Generate the storage section in `%pre` (detect disk size/type) into `/tmp/part.ks`, then `%include /tmp/part.ks`.

## Gotchas
- Validate syntax: `ksvalidator -v <VERSION> ks.cfg` (pykickstart; pick the version name matching the target release).
- Disk names (`sda` vs `nvme0n1`) differ across hardware generations — `%pre` detection avoids per-model files.
- `--recommended` swap can be huge on big-RAM hosts; set an explicit size.

## Verify
- [ ] Test install in a VM with the same disk count; `lsblk` and `findmnt` match the intended layout.

## Checked

2026-10-28

Confirmed: pykickstart kickstart-docs: ignoredisk --only-use and --drives, clearpart, zerombr, autopart (--type values, --nohome, --fstype, --encrypted, --luks-version), reqpart and --add-boot, part, raid, volgroup, logvol (--recommended, --fsoptions, sizes in MiB), %pre with %include, and the ksvalidator -v option in the pykickstart source.

Removed or corrected: The Clevis network-bound-encryption instruction, the RHEL9 version argument, the incomplete autopart type list, and the reqpart description.

Method: documentation only; no commands were run.

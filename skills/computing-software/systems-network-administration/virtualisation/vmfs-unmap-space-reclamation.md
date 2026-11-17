---
id: computing-software.systems-network-administration.virtualisation.vmfs-unmap-space-reclamation
name: vmfs-unmap-space-reclamation
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [unmap, space-reclamation, thin-provisioning, trim, vmfs, vsphere-storage, fstrim, guest-unmap, datastore, vmware, esxi, vsphere]
level: practitioner
status: draft
description: "Reclaim thin-provisioned space end to end: in-guest TRIM/UNMAP, VMFS6 automatic unmap priority and rate, manual esxcli unmap, and overcommit alarms."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage-8-0/storage-provisioning-and-space-reclamation-in-vsphere.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Thin provisioning and space reclamation (UNMAP)

**Goal:** space freed inside guests is actually returned to the array, and thin
overcommit never fills a datastore.

## Two layers of thin
1. **Guest → VMDK:** a thin VMDK only shrinks if the guest issues TRIM/UNMAP and the
   virtual hardware passes it (VM hardware 11+, thin disk; Windows sees thin disks as
   SSD-like; Linux needs `discard` mount option or a periodic `fstrim`).
2. **VMFS → array LUN:** VMFS6 sends UNMAP to a thin LUN for freed blocks automatically
   (space reclamation priority Low by default, rate configurable 100-2000 MB/s).

## Guest side
- Windows: Optimize Drives runs retrim on a schedule (`Optimize-Volume -DriveLetter D -ReTrim`).
- Linux: enable `fstrim.timer` (`systemctl enable --now fstrim.timer`) rather than the
  `discard` mount option on busy filesystems.
- Check: after deleting a large file and trimming, the VMDK size on the datastore drops.

## Datastore side
```sh
esxcli storage vmfs reclaim config get -l <datastore>
esxcli storage vmfs reclaim config set -l <datastore> -p low          # or none
esxcli storage vmfs reclaim config set -l <datastore> -m fixed -b 500   # MB/s
esxcli storage vmfs unmap -l <datastore>      # manual (VMFS5, or to force)
esxcli storage core device vaai status get -d naa.<id>   # Delete Status: supported
```
VMFS5 has no automatic UNMAP; run manual unmap off-hours or migrate to VMFS6 (new
datastore + Storage vMotion; there is no in-place upgrade).

## Overcommit controls
- Alarm on datastore usage (warn 75-80%, critical 85-90%) **and** on provisioned
  vs capacity ratio.
- Snapshots and swap files (`.vswp` = configured RAM minus reservation) consume space too.
- When a thin LUN on the array fills, all VMs on it pause with "no space" questions.

## Gotchas
- Some arrays slow down under heavy UNMAP; keep priority low or set a fixed rate.
- Thick-eager VMDKs never reclaim; that is intended for latency-sensitive apps.
- Encrypted VMs and some backup snapshot states block guest UNMAP passing through.

## Verify
Array-reported used capacity tracks VMFS used capacity within a few percent after a week;
`esxcli storage vmfs reclaim config get` shows priority not "none" on thin LUNs.

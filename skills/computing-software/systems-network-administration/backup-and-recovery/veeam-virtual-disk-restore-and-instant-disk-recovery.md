---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-virtual-disk-restore-and-instant-disk-recovery
name: veeam-virtual-disk-restore-and-instant-disk-recovery
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, instant-disk-recovery, virtual-disk-restore, vmdk-restore, vpower-nfs]
level: practitioner
status: docs-checked
description: "Restore individual VMDKs with Veeam virtual disk restore, or attach disks instantly from backup with Instant Disk Recovery and migrate them to production storage."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/instant_disk_recovery.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Instant Disk Recovery (Veeam)

## When to use it
Instant Disk Recovery restores VM disks (not the whole VM) from a backup and publishes them in their initial format.
- Recovering a whole VM: use Instant Recovery to VMware vSphere instead.
- Recovering disks while the target VM stays powered on: Instant Disk Recovery. If the VM can be turned off, use Virtual Disk Restore.
- To register disks as First Class Disks, see Instant First Class Disk (FCD) Recovery. Disks can also be recovered from storage snapshots.

## How it works (vPower)
1. Veeam checks that the vPower NFS datastore is mounted on the ESXi host and holds the VMDK files of the recovered disks.
2. If you replace an existing disk, it unmounts and deletes that disk.
3. It connects the recovered disks to the target VM.
4. It creates a protective snapshot of the target VM, so a failed process loses no data.
5. Changes to the recovered disks are written to redo logs on the vPower NFS server.

## Finalising
The process must be finalised: test the recovered disks, then either migrate them to production (Veeam uses the Quick Migration mechanism) or stop publishing them.

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center page "Instant Disk Recovery". The earlier text said migration uses Storage vMotion; the page says Quick Migration, so it was corrected.
Removed (not on the page): the Virtual Disk Restore wizard options, menu paths, the situation table, deduplicating-appliance I/O and NFS write-cache warnings, `Get-Disk`/`lsblk` Verify steps. Virtual Disk Restore needs its own page and is not covered here.
Method: documentation only; no commands were run.

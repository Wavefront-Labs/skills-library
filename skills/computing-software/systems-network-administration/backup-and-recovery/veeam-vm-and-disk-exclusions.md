---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-vm-and-disk-exclusions
name: veeam-vm-and-disk-exclusions
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, veeam-exclusions, disk-exclusion, vm-exclusion, backup-scope, independent-disks]
level: practitioner
status: draft
description: "Exclude VMs, containers, virtual disks and guest folders from Veeam jobs correctly, and avoid the traps with tags, independent disks and restore of excluded disks."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/overview.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/overview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM and disk exclusions

Job > Virtual Machines > **Exclusions** button.

## VM exclusions
- When a job protects a container (cluster, folder, datastore, tag), exclude individual VMs here; new VMs in the container are picked up automatically, excluded ones stay out.
- Prefer tags for inclusion (e.g. `Backup:Gold`) and an exclusion tag (`Backup:None`) so the policy lives in vCenter.
- Excluding the backup proxy VMs and vCLS VMs keeps noise out.

## Disk exclusions
- Choose: all disks, **0:0 only (system)**, or specific disks by controller:slot (e.g. SCSI 0:1).
- Option "Remove excluded disks from VM configuration" removes them from the backed-up VMX so restored VMs boot without missing-disk errors. Requires the VM to be processed by a supported transport mode.
- Independent disks and RDMs in physical mode are always skipped (no snapshot possible); back them up with an agent or exclude knowingly.

## Guest file exclusions
Guest Processing > Guest file system exclusions: exclude folders or masks (e.g. `*.tmp`, `%TEMP%`). Needs guest credentials and adds processing time; use disk exclusion for whole volumes instead.

## Gotchas
- Exclusions are per job; a VM excluded here may still be in another job.
- Excluded disks cannot be restored later, so confirm with the app owner and record it in the backup scope register.
- Changing the disk set triggers a full read of newly included disks.

## Verify
The job's restore point shows only the expected disks (Restore > Virtual disks wizard lists them); unprotected-VM reports (Veeam ONE) do not flag the excluded VMs unexpectedly.

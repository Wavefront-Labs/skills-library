---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-instant-vm-recovery
name: veeam-instant-vm-recovery
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, veeam-restore, instant-recovery, vpower-nfs, mount-server, quick-migration, storage-vmotion, rto]
level: practitioner
status: docs-checked
description: "Veeam Instant Recovery to vSphere: vPower mount from backup, redo logs and write redirection, migration by Storage vMotion or Quick Migration, source backup types."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/instant_recovery.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Veeam Instant VM Recovery

**Goal:** a failed workload running again within minutes straight from its backup, then moved to production storage.

## How it works
- Veeam Backup & Replication uses vPower to mount the workload image to an ESXi host directly from a compressed and deduplicated backup file; no extraction to production storage is needed.
- The image stays read-only. By default, changes to virtual disks while the recovered VM runs are logged to redo log files on the NFS server (backup server or backup repository); they are discarded when the recovered VM is removed, or merged if you migrate it to production.
- To improve I/O performance you can redirect changes to a datastore closer to the host. Veeam then triggers a snapshot and puts it in the Veeam IR directory on that datastore, with metadata files holding the changes.
- The recovered VM is a "temporary spare" with limited I/O performance; full performance requires migrating it to the production site.
- Several workloads can be recovered at once (bulk processing); Veeam uses resource scheduling to allocate resources.

## Source backups
Instant Recovery to VMware vSphere accepts backups of vSphere, VMware Cloud Director and Hyper-V VMs made by Veeam Backup & Replication, Veeam Agent for Windows/Linux backups, and backups of Nutanix AHV, Amazon EC2, Azure, Google Compute Engine, oVirt, Proxmox VE, Scale Computing HyperCore, HPE Morpheus VM Essentials, Xen and KubeVirt workloads made by the matching Veeam product or plug-in.

## Migrating to production
- **Storage vMotion**: moves the VM with no downtime, pulling data from the NFS datastore and consolidating changes while it runs. It can only be used if you chose to keep changes on the NFS datastore, not redirect them, and it needs the appropriate VMware licence.
- **Quick Migration**: two-stage; recovers the VM from the backup file on the production server, then moves and consolidates the changes.

Instant Recovery also works for DR testing: boot from the backup and check the guest OS and applications without extracting the image.

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center page "Instant Recovery to VMware vSphere" (build 13.x): vPower mount, read-only image, redo logs on the NFS server, redirect to a datastore, Storage vMotion limitation and licence, Quick Migration, supported backup types, bulk processing.
Removed (not on the page): menu paths and step list, "recommended" redirect datastore advice, NFS port and firewall notes, redirect-cache-fill warning, hardened-repository and MAC/UUID notes, performance claims beyond "limited I/O performance", the Verify section. The earlier advice to redirect writes and then use Storage vMotion contradicted the page and was corrected.
Method: documentation only; no commands were run.

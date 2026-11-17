---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-managed-servers-vcenter-and-hyper-v
name: veeam-managed-servers-vcenter-and-hyper-v
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, veeam-managed-server, vcenter, hyper-v, backup-infrastructure, credentials-manager]
level: practitioner
status: docs-checked
description: "Add VMware vSphere servers to Veeam: why to add vCenter rather than standalone ESXi hosts, so jobs follow migrated VMs."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/add_vmware_server.html
  - https://helpcenter.veeam.com/docs/backup/hyperv/add_hyperv_server.html
  - https://helpcenter.veeam.com/docs/backup/permissions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Veeam managed servers: vCenter and ESXi

**Goal:** add VMware vSphere servers to the backup infrastructure as sources and targets for backup, replication and other activities.

## Guidance from the Veeam guide
- You can add vCenter Servers and ESXi hosts.
- If an ESXi host is managed by a vCenter Server, add the **vCenter Server**, not the standalone host. When VMs move between hosts under that vCenter, you do not need to reconfigure jobs: Veeam locates migrated VMs and continues processing them.
- Connecting vCenter instead of standalone hosts gives more flexibility.
- Servers can be added from the console or the web UI (separate sections in the guide).

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center page "Adding VMware vSphere Servers".
Removed (the pages read did not cover them): the Hyper-V, SCVMM and SMB3 notes, required vCenter permissions, port and certificate-thumbprint steps, Credentials Manager and rescan advice, troubleshooting list, Verify section. The Hyper-V source URL redirected to the product overview, and the permissions page was an empty stub.
Method: documentation only; no commands were run.

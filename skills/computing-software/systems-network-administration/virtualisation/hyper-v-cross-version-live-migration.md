---
id: computing-software.systems-network-administration.virtualisation.hyper-v-cross-version-live-migration
name: hyper-v-cross-version-live-migration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [cross-version-live-migration, live-migration, cluster-os-rolling-upgrade, hyper-v]
level: advanced
status: docs-checked
description: "Live migrate Hyper-V VMs between hosts on different Windows Server versions: supported directions, configuration versions, Update-VMVersion timing and pitfalls."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/deploy/upgrade-virtual-machine-version-in-hyper-v-on-windows-or-windows-server
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/cluster-operating-system-rolling-upgrade
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/configure-processor-compatibility-mode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-version live migration

**Goal:** move running VMs from older to newer Hyper-V hosts during upgrades without downtime, and keep a way back until committed.

## Rules
- Cluster OS rolling upgrade moves a cluster only to the next newer Windows Server version (for example 2022 to 2025); for several versions repeat the process, or migrate to a new cluster. The cluster stays in mixed-OS mode and can be reverted until the cluster functional level is updated.
- A VM's **configuration version** must be supported by the destination. Newer hosts support older versions; older hosts reject newer versions.
```powershell
Get-VMHostSupportedVersion                         # on each host
Get-VM | Select Name, Version, Generation
```

## Upgrade workflow
1. Upgrade or add new-version hosts.
2. Live migrate VMs to them (shared-nothing or within the cluster during rolling upgrade). VMs keep the old configuration version and can still move back.
3. When all hosts are on the new version and the cluster functional level is updated with `Update-ClusterFunctionalLevel`, update VM versions in a maintenance window. Before that, the VM runs on either version of host:
```powershell
Stop-VM app01; Update-VMVersion -Name app01 -Force; Start-VM app01
```
Update the version only when you are sure the VM will not need to move back to a host running an earlier Windows version; it must be shut down first. The newest version supported by a host is shown by `Get-VMHostSupportedVersion`.

## Pitfalls
- Processor compatibility mode may be needed if CPU generations differ; it cannot be changed while the VM is running.
- VMs with a configuration version older than 8.0 cannot run on a Windows Server 2022 or newer cluster; update the version first.
- Live migration authentication (Kerberos delegation or CredSSP) must be configured on hosts that are not clustered.

## Verify
After migration, the VM runs on the new host with unchanged configuration version; after the update, `Get-VM` shows the new version and backups still succeed.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: newer hosts import older configuration versions and older hosts cannot import newer ones; Update-VMVersion needs the VM shut down and is only advised when the VM will not move back; rolling upgrade goes one version at a time, is reversible until the functional level is updated, and VMs older than version 8.0 cannot run on Windows Server 2022 or newer; processor compatibility mode cannot be changed on a running VM. Removed as unconfirmed: the list of features unlocked by a version update, the backup software and integration services remarks.

Method: documentation only; no commands were run.

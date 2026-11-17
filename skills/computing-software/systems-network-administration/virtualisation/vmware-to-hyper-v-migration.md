---
id: computing-software.systems-network-administration.virtualisation.vmware-to-hyper-v-migration
name: vmware-to-hyper-v-migration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmware-to-hyper-v, v2v, scvmm, windows-admin-center, hyper-v, vmware, migration-planning]
level: advanced
status: docs-checked
description: "Plan and run VMware-to-Hyper-V migrations: WAC VM Conversion extension, System Center VMM, Azure Migrate for Azure Local, pre-checks, generation mapping, cutover."
sources:
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/use/vm-conversion-extension-overview
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/use/migrate-virtual-machines-vm-conversion-extension
  - https://learn.microsoft.com/en-us/azure/azure-local/concepts/compare-windows-server
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/should-i-create-a-generation-1-or-2-virtual-machine-in-hyper-v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VMware to Hyper-V migration

**Goal:** move VMs from vSphere to Hyper-V with predictable downtime.

## Tool options
Microsoft's comparison page lists these VMware migration methods:
| Target | Method |
|---|---|
| Windows Server Hyper-V | **VM Conversion extension for Windows Admin Center** (preview at the time of review) |
| Windows Server Hyper-V | **System Center Virtual Machine Manager** VMware conversion |
| Azure Local | **Azure Migrate** |
Backup-product restores and manual disk conversion tools are also used in practice; follow each vendor's own
documentation for those.

## VM Conversion extension (WAC) in brief
- Migrates VMware VMs from vCenter (versions 6.x, 7.x and 8.x) to Hyper-V, Windows and Linux, with online
  replication and minimal downtime; no extra cost. It is a **preview** governed by the Windows Admin Center
  pre-release extension terms, with no Microsoft support obligation.
- Workflow: **synchronisation** (initial full copy while the source keeps running, using a snapshot on the source and
  writing VHDX files), then **migration** (Change Block Tracking delta syncs, source powered off, final delta sync,
  VM imported into Hyper-V with CPU, memory and network settings).
- Up to 10 VMs per batch; cluster-aware migration to Windows Server failover clusters; static IP configuration
  preserved; Secure Boot and UEFI template configured by guest OS type; prechecks; multi-disk support; multiple
  vCenter connections.
- Removes VMware Tools from Windows VMs after migration. For **Linux guests, install the Hyper-V drivers before
  starting** or the VM may not boot after migration.
- Supported guests listed include Windows Server 2012 R2 to 2025, Windows 10 and 11, Ubuntu 20.04 and 24.04, Debian
  11 and 12, and some RHEL-based distributions: check the page for the current list.
- Best practice: place the Windows Admin Center gateway in the same site as the ESXi and Hyper-V hosts.

## Pre-migration checklist per VM
1. Firmware: BIOS VMs fit **Generation 1**; Generation 2 uses UEFI firmware, so check the VM is UEFI-capable before
   choosing it (Microsoft's generation page lists what Generation 2 requires).
2. Record IPs, VLANs and any licensing tied to MAC addresses.
3. Remove snapshots; confirm there are no raw device mappings and plan them separately.
4. Check the guest OS is on the supported list of the tool you chose.
5. Linux: install Hyper-V drivers first (WAC extension requirement above).

## Cutover
- Final shutdown of the source (the WAC extension powers it off for you), final sync, power on in Hyper-V, connect
  the right switch and VLAN, re-apply a static IP if it was not preserved.
- Keep the source VM powered off but intact until sign-off.

## Post-migration
- Check integration services with `Get-VMIntegrationService -VMName <name>`.
- Remove leftover VMware devices and tools if the tool did not.
- Update backup, monitoring and CMDB records.

## Verify
App owner sign-off, a backup job succeeds on the new VM, and the VMware copy is deleted only after an agreed
retention period.

## Checked

Date checked: 2026-10-27. Documentation: "VM Conversion extension in Windows Admin Center (Preview)" (ms.date 2025-08-13), the Windows Admin Center migration walkthrough, the Azure Local comparison page (2026-03-02), and the Hyper-V generation 1 versus 2 page.
Confirmed: preview status and licence terms; vCenter 6.x to 8.x; synchronisation and migration phases using Change Block Tracking; batch size of 10; features listed; VMware Tools removal on Windows VMs; Linux Hyper-V drivers prerequisite; VMware migration methods per target. The System Center VMM conversion page was only confirmed as a link from the comparison page.

Method: documentation only; no commands were run.

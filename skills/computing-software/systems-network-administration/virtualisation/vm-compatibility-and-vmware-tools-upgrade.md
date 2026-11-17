---
id: computing-software.systems-network-administration.virtualisation.vm-compatibility-and-vmware-tools-upgrade
name: vm-compatibility-and-vmware-tools-upgrade
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vm-hardware-version, vm-compatibility-upgrade, vmware-tools-upgrade, vmware-tools, open-vm-tools, scheduled-upgrade, vsphere-vm-administration, vmware, vsphere]
level: practitioner
status: draft
description: "Upgrade VM hardware version (compatibility) and VMware Tools safely: order of operations, scheduled upgrades at reboot, open-vm-tools on Linux, and rollback."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1003746
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM compatibility (hardware version) and VMware Tools upgrades

**Goal:** VMs get new virtual hardware features and current drivers without unplanned
outages or broken NICs.

## Order of operations
1. Upgrade **ESXi hosts** in the cluster first.
2. Upgrade **VMware Tools** in the guest (drivers for VMXNET3/PVSCSI, quiescing, time).
3. Only then, if a feature needs it, upgrade the **VM compatibility** (hardware version),
   which requires a power cycle and cannot be downgraded.

## Do you need a newer hardware version?
Upgrade only when you need a feature (more vCPU/RAM, vTPM, precision clock, newer
virtual NVMe, vGPU features, per-VM EVC). Upgrading pins the VM to hosts that support
that version: a vmx-21 VM cannot run on ESXi 7, which matters for DR sites and
cross-vCenter moves. Keep templates at the oldest version your DR site supports.

## VMware Tools
- **Windows:** upgrade from vCenter (Upgrade VMware Tools, automatic or interactive), or
  via your software deployment tool using the Tools installer with
  `setup64.exe /S /v "/qn REBOOT=R"`. A reboot is usually needed for driver updates.
- **Linux:** use **open-vm-tools** from the distro repo and patch it with the OS; vCenter
  shows "Guest Managed". Do not install the legacy tar Tools on modern distros.
- **Upgrade at power cycle:** VM → Compatibility → Schedule VM Compatibility Upgrade, or
  Tools "Check and upgrade VMware Tools before each power on", then reboot in the next
  patch window.

## Gotchas
- Windows guests sometimes come back after a hardware upgrade with a **new NIC** (ghost
  adapter) and lose a static IP. Record IP config first; remove hidden devices if needed.
- Snapshot before a compatibility upgrade so you can revert (it is the only rollback).
- Tools version alarms ("out of date") are cosmetic until a security advisory lists Tools;
  then treat them as patches.

## Report
```powershell
Get-VM | Select Name, HardwareVersion, @{n='Tools';e={$_.Guest.ToolsVersion}},
  @{n='ToolsStatus';e={$_.ExtensionData.Guest.ToolsVersionStatus2}} | Sort HardwareVersion
```

## Verify
Tools status "Current" or "Guest Managed" for all VMs; hardware versions consistent with
the DR site's ESXi version; no VM lost its network after the change.

---
id: computing-software.systems-network-administration.virtualisation.esxi-host-licensing-and-evaluation-mode
name: esxi-host-licensing-and-evaluation-mode
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-license, vsphere-licensing, vcenter-licensing, evaluation-mode, vmware, esxi, vsphere]
level: practitioner
status: docs-checked
description: "Assign and track vSphere/ESXi licences in vCenter or on a standalone host, handle the 60-day evaluation, and what stops working when a licence expires."
sources:
  - https://knowledge.broadcom.com/external/article/313548
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-and-host-management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESXi host licensing and evaluation mode

**Goal:** every host and vCenter licensed before evaluation runs out, with features that match the licence edition.

## Evaluation mode
- New ESXi and vCenter installs start in evaluation mode with the full feature set until
  the evaluation period expires.
- When evaluation expires on a host: running VMs keep running, but you cannot power on VMs, and the host disconnects from vCenter if vCenter cannot license it.
- Free ESXi (where offered) has a read-only API: PowerCLI and backup tools cannot write.

## Assign in vCenter
Administration -> Licensing -> Licenses -> Add (paste keys) -> Assets -> Hosts -> Assign License. PowerCLI:
```powershell
$lm  = Get-View LicenseManager
$lam = Get-View $lm.LicenseAssignmentManager
$lam.UpdateAssignedLicense((Get-VMHost esx01).ExtensionData.MoRef.Value, '<KEY>', $null)
Get-VMHost | Select Name, LicenseKey
```
With VCF/VVF subscription licensing, usage is counted per core and shown in the vCenter licensing views (see the VVF/VCF licensing KB).

## Standalone host
Host Client -> Manage -> Licensing -> Assign license.

## Core-based licensing rules
- Per-core licensing with a 16-core minimum per CPU socket; a 2 x 12-core host consumes 32 cores.
- Edition gates features: DRS, vDS, Storage vMotion, host profiles need the higher editions. Downgrading the key removes them (DRS turns off, vDS ports cannot change).

## Gotchas
- Moving a host to a new vCenter does not move its key; reassign it.
- An expired vCenter licence stops host additions and some management operations.
- Track expiry: the licence page and the `License expiration` alarm; set the alarm to email.

## Verify
`Get-VMHost | Select Name, LicenseKey` shows no `00000-00000...` evaluation keys; licence usage stays within purchased cores.

## Checked
2026-10-31: Confirmed the 16-cores-per-CPU minimum subscription capacity and the
cores-per-socket counting method against Broadcom KB 313548 (VVF/VCF licensing). Replaced
the dead vSphere License Management deep link with the guide root; removed the 60-day
evaluation figure and the vim-cmd vimsvc/license commands (target pages 404 / not
confirmable in fetched pages).
Method: documentation only; no commands were run.

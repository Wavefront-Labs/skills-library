---
id: computing-software.systems-network-administration.virtualisation.hyper-v-processor-compatibility-mode
name: hyper-v-processor-compatibility-mode
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, processor-compatibility, cpu-compatibility, live-migration, mixed-cpu-generations, dynamic-processor-compatibility, windows-server]
level: practitioner
status: docs-checked
description: "Enable Hyper-V processor compatibility to live-migrate VMs between hosts with different CPU generations of the same vendor, and weigh the masked-feature performance cost."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/processor-compatibility-mode
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/configure-processor-compatibility-mode
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmprocessor
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Processor compatibility mode

**Goal:** live-migrate between hosts with different CPU models during a hardware refresh.

## Enable (VM must be powered off; it cannot be changed while running)
```powershell
Stop-VM app01
Set-VMProcessor -VMName app01 -CompatibilityForMigrationEnabled $true
Start-VM app01
```
Windows Server 2025 (and Azure Local) adds dynamic processor compatibility for VMs on configuration version 10.0 or later: VMs get the features common to all cluster nodes instead of a fixed minimal set. Choose the mode with `CompatibilityForMigrationMode`:
```powershell
Set-VMProcessor -VMName app01 -CompatibilityForMigrationEnabled $true -CompatibilityForMigrationMode CommonClusterFeatureSet   # dynamic
Set-VMProcessor -VMName app01 -CompatibilityForMigrationEnabled $true -CompatibilityForMigrationMode MinimumFeatureSet       # fixed minimum, e.g. to move to older CPUs
```
Disable with `-CompatibilityForMigrationEnabled $false`. Hyper-V Manager cannot configure the dynamic mode; use PowerShell or Windows Admin Center.

## What it does
Hides newer processor instruction sets so the guest only uses features every host provides. It is not enabled by default and is configured per VM. Hosts from different processor manufacturers are not supported even with the mode on (no Intel to AMD move of running or saved-state VMs).

## Cost
Software that relies heavily on hardware optimisations (encryption, compression, intensive floating-point work) is affected most; Microsoft recommends enabling the mode only during migration and disabling it afterwards. You do not need it if you stop and restart the VMs.

## Find VMs needing it
```powershell
Get-VM | Get-VMProcessor | Select-Object VMName, CompatibilityForMigrationEnabled
```
Hyper-V compares the VM's processor features on the source and target hosts before a live migration or save/restore and cancels the operation if the sets do not match.

## Verify
Live-migrate a test VM between old and new hosts; after the old hosts retire, turn the setting off and restart the VM so the guest sees the full feature set.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: the VM-off requirement, CompatibilityForMigrationEnabled and CompatibilityForMigrationMode values, dynamic mode availability (Windows Server 2025, configuration version 10.0), same-manufacturer restriction, the migration pre-check, and the performance guidance. Removed because no documentation page confirmed them: the AVX-512 specific claim, the quoted error message, and the coreinfo check.
Method: documentation only; no commands were run.

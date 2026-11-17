---
id: computing-software.systems-network-administration.virtualisation.hyper-v-live-migration-failures-compare-vm
name: hyper-v-live-migration-failures-compare-vm
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [live-migration-failure-events, compare-vm, hyper-v-live-migration, processor-compatibility, kerberos-constrained-delegation, hyper-v]
level: advanced
status: docs-checked
description: "Diagnose failed Hyper-V live migrations: pre-check with Compare-VM, read the VMMS event log, and fix processor, authentication and version incompatibilities."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/compare-vm
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/deploy/set-up-hosts-for-live-migration-without-failover-clustering
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/processor-compatibility-mode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live migration failures

## Pre-check
```powershell
$r = Compare-VM -Name app01 -DestinationHost hv02
$r.Incompatibilities | Format-Table Message, MessageId -AutoSize
```
`Compare-VM` compares a VM and a destination host for compatibility and returns a compatibility report; add
`-IncludeStorage` when storage will move too. Fix every incompatibility it lists, then pass the report to `Move-VM
-CompatibilityReport` if you want to act on it.

## Logs
- `Microsoft-Windows-Hyper-V-VMMS-Admin` on source and destination (use `Get-WinEvent -ListLog *Hyper-V*` to see
  the other Hyper-V logs on the host).
- Clusters: `Get-ClusterLog -Node hv01,hv02 -TimeSpan 10` (minutes back from now).
```powershell
Get-WinEvent -LogName Microsoft-Windows-Hyper-V-VMMS-Admin -MaxEvents 50 |
  Where-Object LevelDisplayName -ne Information | Format-List TimeCreated, Id, Message
```

## Common causes
| Symptom | Cause | Fix |
|---|---|---|
| Processor features differ between hosts | different CPU generations: Hyper-V cancels the migration when the feature sets do not match | `Set-VMProcessor -VMName app01 -CompatibilityForMigrationEnabled $true` with the VM off |
| Moving between Intel and AMD hosts | not possible for running or saved VMs even with compatibility mode | migrate offline or use hosts with the same processor manufacturer |
| "Failed to establish a connection with host ... No credentials are available in the security package 0x8009030E" | CredSSP authentication and you are not signed in to the source server (needed when moving back, too) | sign in to the source server, or use Kerberos with constrained delegation |
| Kerberos failures | constrained delegation missing for `cifs` (storage moves) or `Microsoft Virtual System Migration Service` (VM moves) | configure delegation with a Domain Admin account, then use Kerberos in the host's live migration settings |
| VM configuration version not supported | destination older than the VM version | migrate to an equal or newer host |

## Gotchas
- Compatibility mode must be set while the VM is off; plan the change before the migration window.
- Hyper-V Manager from a third machine needs Kerberos delegation; with CredSSP run the move from the source server.

## Verify
`Compare-VM` shows no incompatibilities; `Move-VM app01 hv02` completes; repeat in reverse.

## Checked

Date checked: 2026-10-27. Documentation: Compare-VM and Move-VM reference (Windows Server 2025 docset), "Set up hosts for live migration without Failover Clustering" and "Processor compatibility mode" pages (windowsserverdocs main branch), Get-ClusterLog reference.
Confirmed: Compare-VM purpose and -IncludeStorage; Move-VM -CompatibilityReport; processor feature-set check and Intel to AMD limit; CredSSP sign-in requirement and the 0x8009030E message; constrained delegation services cifs and Microsoft Virtual System Migration Service; Domain Admin requirement for delegation; -TimeSpan in minutes; Set-VMProcessor -CompatibilityForMigrationEnabled.

Method: documentation only; no commands were run.

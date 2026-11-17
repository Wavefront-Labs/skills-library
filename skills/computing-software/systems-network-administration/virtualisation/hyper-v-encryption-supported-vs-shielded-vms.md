---
id: computing-software.systems-network-administration.virtualisation.hyper-v-encryption-supported-vs-shielded-vms
name: hyper-v-encryption-supported-vs-shielded-vms
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [encryption-supported-vm, shielded-vms, vtpm, hyper-v, security]
level: advanced
status: docs-checked
description: "Compare encryption-supported and shielded Hyper-V VMs: which protections each gives, admin access differences, and how to choose and set the security policy."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-and-shielded-vms
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-tenant-creates-shielding-data
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmsecuritypolicy
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmkeyprotector
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encryption supported vs shielded VMs

**Goal:** choose the right protection level for VMs on a guarded fabric.

## Comparison (Generation 2 VMs)
| Capability | Encryption supported | Shielded |
|---|---|---|
| Secure Boot | Required but configurable | Required and enforced |
| vTPM | Required but configurable | Required and enforced |
| Encrypt VM state and live migration traffic | Required but configurable | Required and enforced |
| Integration components | Configurable by fabric admin | Certain ones blocked (for example data exchange, PowerShell Direct) |
| VMConnect console, HID devices | On, cannot be disabled | Enabled on hosts from Windows Server version 1803, disabled on earlier hosts |
| COM/serial ports | Supported | Disabled, cannot be enabled |
| Attach a debugger to the VM process | Supported | Disabled (the VM worker process is a protected process light; LiveKd-style techniques are not blocked) |

Both types keep live migration, Hyper-V Replica and checkpoints working. A normal Gen 2 VM on the same fabric gets none of these protections.

## Set
```powershell
Set-VMKeyProtector -VMName app01 -KeyProtector $kp.RawData   # HGS key protector
Set-VMSecurityPolicy -VMName app01 -Shielded $false          # encryption supported
Set-VMSecurityPolicy -VMName app02 -Shielded $true           # shielded
Get-VMSecurity -VMName app01,app02
```
In shielding data files use `New-ShieldingDataFile -Policy EncryptionSupported` (vTPM plus basic console and PowerShell Direct) or `-Policy Shielded`.

## Choosing
- **Encryption supported**: fabric admins are fully trusted (for example disks must be encrypted at rest for compliance) and keep day-to-day tools such as the console and PowerShell Direct.
- **Shielded**: data and state must be protected from fabric administrators and from untrusted software on the hosts.

## Gotchas
- Both types depend on HGS (attestation and key release) to start and live migrate on a guarded fabric; plan HGS availability before broad rollout.

## Verify
`Get-VMSecurity` matches the intended policy; console and PowerShell Direct behaviour matches the table.

## Checked

Checked 2026-10-26 against the Guarded fabric and shielded VMs overview and the tenant shielding-data page in MicrosoftDocs/windowsserverdocs (latest commit 2026-10-23), plus the Windows Server 2025 `Set-VMSecurityPolicy` reference. The comparison table now follows Microsoft's table. Wrong in the earlier draft: the console was listed as unavailable for shielded VMs (it is enabled from host version 1803), guest file copy was cited as a blocked component (data exchange and PowerShell Direct are the documented examples), debugger and COM port rows were mis-assigned, and a claim that moving from shielded back to encryption supported needs a re-key was removed as undocumented.

Method: documentation only; no commands were run.

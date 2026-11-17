---
id: computing-software.systems-network-administration.virtualisation.hyper-v-key-protector-and-vtpm
name: hyper-v-key-protector-and-vtpm
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, hyper-v-vtpm, key-protector, vtpm, set-vmkeyprotector, enable-vmtpm, bitlocker, windows-11-vm, windows-server]
level: advanced
status: docs-checked
description: "Add a virtual TPM to Gen 2 Hyper-V VMs with a local or HGS key protector, and update the key protector so the VM can start on another host."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/enable-vmtpm
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmkeyprotector
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-manage-hgs
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/generation-2-virtual-machine-security-features
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key protector and vTPM for Gen 2 VMs

**Goal:** give VMs a virtual TPM (for BitLocker in the guest and other TPM-dependent features) without losing the ability to migrate or restore them.

## Local key protector (no HGS)
```powershell
Stop-VM vm01
Set-VMKeyProtector -VMName vm01 -NewLocalKeyProtector
Enable-VMTPM -VMName vm01
Start-VM vm01
```
Both cmdlets exist in the Hyper-V module (`-NewLocalKeyProtector` generates a new local key protector).

## Move or restore the VM elsewhere
Microsoft's Generation 2 security page: a VM with a vTPM can be migrated to another supported host, but it might not start there until you update its key protector to authorise the new host. Owner and local guardian certificates are created in the machine's store **Shielded VM Local Certificates** (`Cert:\LocalMachine\Shielded VM Local Certificates`); keep backups of them. If a wrong key protector is applied, return to the previous one:
```powershell
Set-VMKeyProtector -VMName vm01 -RestoreLastKnownGoodKeyProtector
```

## HGS-backed key protector (guarded fabric)
```powershell
$owner  = Get-HgsGuardian -Name 'TenantOwner'
$fabric = Get-HgsGuardian -Name 'Fabric'
$kp = New-HgsKeyProtector -Owner $owner -Guardian $fabric -AllowUntrustedRoot
Set-VMKeyProtector -VMName app01 -KeyProtector $kp.RawData
Enable-VMTPM -VMName app01
```
`-AllowUntrustedRoot` is for self-signed guardian certificates.

## Authorise another guardian on an existing VM
Documented in the HGS management page (shut the VM down first, and have the owner do this):
```powershell
$kp = ConvertTo-HgsKeyProtector -Bytes (Get-Content -Path .\VM001.kp)
$updated = Grant-HgsKeyProtectorAccess -KeyProtector $kp -Guardian (Get-HgsGuardian -Name 'NewGuardian')
$updated.RawData | Out-File .\updatedVM001.kp
Set-VMKeyProtector -VMName VM001 -KeyProtector (Get-Content -Path .\updatedVM001.kp)
```
Save the existing protector first with `Get-VMKeyProtector -VMName VM001 | Out-File .\VM001.kp`.

## Gotchas
- Restores and replicas on a new host hit the same authorisation step; put it in the DR runbook.

## Verify
`Get-VMSecurity -VMName vm01` shows the TPM enabled (check its output), and the VM starts after a test migration to each target host.

## Checked

Checked 2026-10-26 against the Windows Server 2025 Hyper-V cmdlet references (`Set-VMKeyProtector` parameters including `-NewLocalKeyProtector` and `-RestoreLastKnownGoodKeyProtector`, `Enable-VMTPM`, `New-HgsKeyProtector`) and MicrosoftDocs/windowsserverdocs (Generation 2 security features page; HGS management page for the key protector update procedure, `RawData`, `Grant-HgsKeyProtectorAccess`). Removed as undocumented: the PFX export/import of local certificates between hosts, the quoted "could not be unwrapped" error text, and the cluster-node certificate claim. Windows 11 and Credential Guard mentions were dropped because the cited pages do not cover them.

Method: documentation only; no commands were run.

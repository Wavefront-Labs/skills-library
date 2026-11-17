---
id: computing-software.systems-network-administration.virtualisation.hyper-v-shielding-data-and-template-disks
name: hyper-v-shielding-data-and-template-disks
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, shielded-vm, shielding-data, shielded-template, protect-templatedisk, volume-signature-catalog, pdk, windows-server]
level: sme
status: docs-checked
description: "Build signed shielded template disks and shielding data (.pdk) files for shielded VMs: owner and fabric guardians, volume ID qualifiers, answer files and deployment."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-create-a-shielded-vm-template
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-tenant-creates-shielding-data
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-create-a-shielded-vm-using-powershell
  - https://learn.microsoft.com/en-us/powershell/module/shieldedvmdatafile/new-shieldingdatafile
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shielding data files and template disks

**Goal:** deploy shielded VMs whose secrets (admin password, certificates, BitLocker keys) the fabric admin can never see.

## 1. Prepare the template disk
- Gen 2 VM prepared as documented: GPT, Basic (not Dynamic) disk, at least two partitions, NTFS, a supported Windows OS, and generalised with sysprep. Template VHDX files cannot use differencing disks or checkpoints.
- Install the `Shielded VM Tools` feature (RSAT-Shielded-VM-Tools) on the authoring machine.
```powershell
$cert = Get-Item Cert:\CurrentUser\My\<thumbprint>       # signing cert
Protect-TemplateDisk -Path 'ws2022-template.vhdx' -TemplateName 'WS2022 DC' -Version 1.0.0.0 -Certificate $cert
Save-VolumeSignatureCatalog -TemplateDiskPath 'ws2022-template.vhdx' -VolumeSignatureCatalogPath 'ws2022.vsc'
```
Protect-TemplateDisk modifies the VHDX in place and a protected disk cannot be modified afterwards; keep an unprotected copy for updates. Only use the result with the shielded provisioning process (booting it as a normal VM is unsupported).

## 2. Guardians
```powershell
$owner  = New-HgsGuardian -Name 'TenantOwner' -GenerateCertificates
# fabric guardian from HGS metadata: http://<HGS cluster name>/KeyProtection/service/metadata/2014-07/metadata.xml
$fabric = Import-HgsGuardian -Path 'fabric-metadata.xml' -Name 'Fabric'
```
Back up the owner guardian's certificates: they are the break-glass key for every VM it owns.

## 3. Shielding data file
```powershell
$vidq = New-VolumeIDQualifier -VolumeSignatureCatalogFilePath 'ws2022.vsc' -VersionRule GreaterThanOrEquals
New-ShieldingDataFile -ShieldingDataFilePath 'tenant.pdk' -Owner $owner -Guardian $fabric `
  -VolumeIDQualifier $vidq -AnswerFile 'unattend.xml' -Policy Shielded
```
`-Policy EncryptionSupported` gives a vTPM-enabled VM that allows basic console connections and PowerShell Direct. If guardian certificates are self-signed or expired, `Import-HgsGuardian` may need `-AllowUntrustedRoot` and/or `-AllowExpired`.

## 4. Deploy
```powershell
New-ShieldedVM -Name 'dc03' -TemplateDiskPath 'ws2022-template.vhdx' -ShieldingDataFilePath 'tenant.pdk' -Wait
```
`New-ShieldedVM` comes from the `GuardedFabricTools` module (`Install-Module GuardedFabricTools -Repository PSGallery`) on the guarded host; add `-Linux` for Linux templates. SCVMM can do the same.

## Gotchas
- Answer files are reused for every VM from the shielding data file, so do not hard-code VM-specific values; substitution strings such as `@ComputerName@` are replaced at provisioning (VMM and `New-ShieldedVM -SpecializationValues` supply values).
- VolumeIDQualifier `Equals` trusts only the exact template version; `GreaterThanOrEquals` trusts later versions too.

## Verify
The VM provisions, the guest OS volume is BitLocker protected by the vTPM, and Shielded-policy VMs refuse PowerShell Direct.

## Checked

Checked 2026-10-26 against MicrosoftDocs/windowsserverdocs guarded-fabric pages (latest commit 2026-10-23) and the Windows Server 2025 `New-ShieldingDataFile`, `New-VolumeIDQualifier` and `Protect-TemplateDisk` references. Confirmed: `Protect-TemplateDisk` and `Save-VolumeSignatureCatalog` syntax, `New-ShieldingDataFile -AnswerFile/-Policy/-VolumeIDQualifier`, `-VersionRule Equals/GreaterThanOrEquals`, `RSAT-Shielded-VM-Tools`, metadata URL pattern, template disk prerequisites, in-place modification, and policy semantics. Corrected: `New-ShieldedVM` is a GuardedFabricTools module cmdlet, not built in; the console statement was dropped because Microsoft's table says console is enabled for shielded VMs from host version 1803.

Method: documentation only; no commands were run.

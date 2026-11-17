---
id: computing-software.systems-network-administration.virtualisation.hyper-v-shielded-linux-vms
name: hyper-v-shielded-linux-vms
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [shielded-linux-vm, shielded-vms, linux, host-guardian-service, hyper-v]
level: advanced
status: docs-checked
description: "Deploy shielded Linux VMs on a Hyper-V guarded fabric: supported distributions, preparing and signing a Linux template disk, shielding data and limits."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-create-a-linux-shielded-vm-template
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-create-a-shielded-vm-using-powershell
  - https://learn.microsoft.com/en-us/powershell/module/shieldedvmtemplate/protect-templatedisk
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shielded Linux VMs

**Goal:** Linux workloads with the same fabric-admin protection as shielded Windows VMs.

## Support
Preparing a Linux template needs a server running Windows Server, version 1709 or later (Windows Server 2019 RSAT also works for `Protect-TemplateDisk`). Microsoft's page lists Ubuntu 16.04 LTS with the 4.4 kernel, Red Hat Enterprise Linux 7.3 and SUSE Linux Enterprise Server 12 SP2, and warns that newer releases of these OSes may hit a TPM driver bug that stops them provisioning as shielded VMs. Re-check that page for the current list.

## Template disk preparation
1. Create a new Gen 2 VM (UEFI) with no differencing disk and install the distribution with a GPT layout, the root partition encrypted with dm-crypt using the passphrase `passphrase` (it is randomised when a shielded VM is provisioned) and an ext2 boot partition. An existing unencrypted VM cannot be reused because Linux disk encryption is set at partitioning time.
2. Install the `lsvmtools` package from the distribution's package manager (bootloader shim, provisioning components, disk preparation tool), customise the OS, install an SSH server, delete all checkpoints, then run `lsvmprep` (the installed path varies by version).
3. Shut down and, on a Windows Server with the Shielded VM Tools feature (`Install-WindowsFeature RSAT-Shielded-VM-Tools`), sign the disk:
```powershell
Protect-TemplateDisk -Path .\ubuntu-template.vhdx -TemplateName 'Ubuntu LTS' -Version 1.0.0.0 `
  -Certificate $signingCert -ProtectedTemplateTargetDiskType PreprocessedLinux
```
4. Extract the volume signature catalog and give it to VM owners:
```powershell
Save-VolumeSignatureCatalog -TemplateDiskPath .\ubuntu-template.vhdx -VolumeSignatureCatalogPath .\ubuntu-template.vsc
```

## Shielding data
Create a shielding data file (`.pdk`) with `New-ShieldingDataFile` (owner guardian, HGS guardians, volume ID qualifier from the template's catalog, and an answer file). For a Linux PDK, run the cmdlets on a server running Windows Server, version 1709 or later; the Linux answer file format differs from `unattend.xml`.

## Provisioning
Use a fabric manager such as SCVMM, or on a guarded host the `New-ShieldedVM` cmdlet from the `GuardedFabricTools` PowerShell Gallery module, adding `-Linux`:
```powershell
New-ShieldedVM -Name 'MyLinuxVM' -TemplateDiskPath .\ubuntu-template.vhdx -ShieldingDataFilePath .\tenant.pdk -Wait -Linux
```

## Limits
- No console access; ensure SSH works through the answer file before rollout.
- Microsoft advises not updating templates or shielded VMs to newer OS releases than the listed ones until the TPM driver bug is fixed.

## Verify
The VM boots on a guarded host, `Get-VMSecurity` reflects the shielded policy, you can reach it over SSH, and the root volume is on a dm-crypt device.

## Checked

Checked 2026-10-26 against MicrosoftDocs/windowsserverdocs (latest commit 2026-10-23): Create a Linux shielded VM template disk, Create a shielded VM using PowerShell, and the Windows Server 2025 `Protect-TemplateDisk` / `New-ShieldingDataFile` references. Wrong in the earlier draft: the supported distributions were not named (Ubuntu 16.04 4.4 kernel, RHEL 7.3, SLES 12 SP2 are the documented ones), the partition layout was wrong (dm-crypt root with the documented passphrase and an ext2 boot partition), the `MicrosoftUEFICertificateAuthority` Secure Boot template step is not in the page and was removed, `New-ShieldedVM` comes from the GuardedFabricTools module and needs `-Linux`, and the Linux answer-file contents and kernel-update guidance were unconfirmed and removed.

Method: documentation only; no commands were run.

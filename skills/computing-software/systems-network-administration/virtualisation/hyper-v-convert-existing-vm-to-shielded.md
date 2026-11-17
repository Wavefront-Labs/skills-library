---
id: computing-software.systems-network-administration.virtualisation.hyper-v-convert-existing-vm-to-shielded
name: hyper-v-convert-existing-vm-to-shielded
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [convert-to-shielded, shielded-vms, vtpm, host-guardian-service, hyper-v]
level: advanced
status: docs-checked
description: "Convert an existing Gen 2 Windows Hyper-V VM to a shielded VM: documented prerequisites, shielding helper VHD, guardians, key protector, shielding data and checkpoints."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-vm-shielding-helper-vhd
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-shielded-vm-planning-for-tenants
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-shielded-vm-windows-azure-pack
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmsecuritypolicy
  - https://learn.microsoft.com/en-us/powershell/module/shieldedvmdatafile/new-shieldingdatafile
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Convert an existing VM to shielded

**Goal:** protect an already-running Windows workload with shielding, without rebuilding it.

## Prerequisites (documented)
- Guest OS Windows Server 2012, 2012 R2, 2016 or a Semi-Annual Channel release. **Existing Linux VMs cannot be converted**; build Linux shielded VMs from a signed Linux template instead.
- Generation 2 VM (UEFI) whose OS volume does not use differencing disks.
- A guarded fabric: hosts that attest successfully (`Get-HgsClientConfiguration` shows `IsHostGuarded` True).
- The hosting provider prepares a **VM shielding helper VHD** once (`Initialize-VMShieldingHelperVHD -Path <helper.vhdx>` on a machine with the Shielded VM Tools feature), copies it to the VMM library and sets it under Host Guardian Service Settings in VMM. Do not boot the helper's source VM again afterwards, and do not reuse a template disk for it (GPT disk identifier collision).
- Delete old checkpoints first: existing checkpoints and backups of a converted VM are not encrypted.

## Steps
1. Create guardians and a shielding data file for the existing VM. `New-ShieldingDataFile` has a separate existing-VM parameter set that needs only the owner, guardians and policy (no volume ID qualifier or answer file):
```powershell
$owner = New-HgsGuardian -Name 'Owner' -GenerateCertificates      # back up its certificates
$hgs   = Import-HgsGuardian -Path .\hgs.xml -Name 'HGS'           # metadata from the HGS server
New-ShieldingDataFile -ShieldingDataFilePath .\existing.pdk -Owner $owner -Guardian $hgs -Policy Shielded
```
Fetch the guardian metadata from `http://<HGS cluster name>/KeyProtection/service/metadata/2014-07/metadata.xml`. Add `-AllowUntrustedRoot` to `Import-HgsGuardian` only for self-signed lab certificates.
2. Shield the VM through the fabric manager (SCVMM, or Windows Azure Pack) using that shielding data. The helper VHD is what performs the conversion and BitLocker encryption.
3. The per-VM building blocks that the conversion applies are `Set-VMKeyProtector -KeyProtector <bytes>`, `Set-VMSecurityPolicy -Shielded $true` and `Enable-VMTPM`; Microsoft documents the helper-VHD route for converting existing Windows VMs, so use it rather than applying these cmdlets by hand to a running workload.

## Effects of shielding
- Shielded VMs block PowerShell Direct, data exchange and other integration components, COM ports and traditional debuggers; fabric admins cannot inspect or tamper with the VM.
- VMConnect console connections are enabled for shielded VMs on hosts from Windows Server version 1803 and disabled on earlier hosts.
- The VM only runs on hosts that pass attestation.

## Gotchas
- Back up the owner guardian certificates (store: Shielded VM Local Certificates on the machine that generated them); Microsoft's samples warn not to lose them.
- Keep network access (RDP/SSH) to the guest working before conversion.

## Verify
`Get-VMSecurity -VMName app01` reflects the shielded policy, the guest reports BitLocker protection on its OS volume, and the VM refuses PowerShell Direct.

## Checked

Checked 2026-10-26 against MicrosoftDocs/windowsserverdocs (guarded-fabric-shielded-vm folder, latest commit 2026-10-23) and the Windows Server 2025 Hyper-V and ShieldedVMDataFile cmdlet references. Confirmed: guest OS list and the statement that Linux VMs cannot be converted, Gen 2 and no differencing disk, helper VHD procedure and `Initialize-VMShieldingHelperVHD`, checkpoint and backup warning, `New-ShieldingDataFile` existing-VM parameter set, guardian metadata URL, `-AllowUntrustedRoot` use, console behaviour by host version. Removed: the in-place cmdlet-only conversion recipe and the exact property names of `Get-VMSecurity` output, which the reference does not document.

Method: documentation only; no commands were run.

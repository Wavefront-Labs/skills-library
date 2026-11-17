---
id: computing-software.systems-network-administration.virtualisation.hyper-v-shielded-vm-attestation-modes
name: hyper-v-shielded-vm-attestation-modes
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, shielded-vm, guarded-fabric, tpm-attestation, host-key-attestation, host-guardian-service, code-integrity-policy, windows-server]
level: sme
status: docs-checked
description: "Choose and configure guarded-host attestation for shielded VMs: TPM-trusted attestation with baselines and CI policies, or host key attestation, and register hosts with HGS."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-and-shielded-vms
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-initialize-hgs-tpm-mode-default
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-initialize-hgs-key-mode-default
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-create-host-key
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-tpm-trusted-attestation-capturing-hardware
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-confirm-hosts-can-attest-successfully
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TPM vs host key attestation

**Goal:** let only healthy, authorised Hyper-V hosts start shielded VMs.

| Mode | Proves | Requirements |
|---|---|---|
| TPM-trusted | Host identity (TPM EK), Measured Boot sequence (TCG log baseline), code integrity policy | TPM 2.0, UEFI 2.3.1 with Secure Boot, IOMMU and SLAT, a code integrity policy |
| Host key (WS2019+) | Possession of a registered key | A key pair or certificate (at least 2048-bit RSA, Client Authentication EKU, Digital Signature usage if custom); no health measurement |
| Admin-trusted (legacy) | Membership of an AD security group | Deprecated beginning with Windows Server 2019 |

Microsoft recommends TPM-trusted attestation where hardware allows; you can switch HGS between modes later. TPM-trusted hosts attest at start and every 8 hours.

## Initialise HGS
```powershell
Initialize-HgsServer -HgsServiceName 'MyHgsDNN' -SigningCertificateThumbprint '<thumbprint>' -EncryptionCertificateThumbprint '<thumbprint>' -TrustTpm   # or -TrustHostKey
```

## Register a TPM host
On the host:
```powershell
(Get-PlatformIdentifier -Name 'hv01').InnerXml | Out-File hv01-ek.xml -Encoding UTF8
Get-HgsAttestationBaselinePolicy -Path 'hw-gen10.tcglog'     # once per hardware/firmware class; -SkipValidation if the reference host lacks Secure Boot, IOMMU, VBS or a CI policy
# Code integrity policy: build in audit mode, test, then enforce; ConvertFrom-CIPolicy -XmlFilePath <x>.xml -BinaryFilePath <x>.p7b
```
On HGS:
```powershell
Add-HgsAttestationTpmHost   -Path hv01-ek.xml -Name hv01
Add-HgsAttestationTpmPolicy -Path hw-gen10.tcglog -Name 'Gen10-Baseline'
Add-HgsAttestationCIPolicy  -Path HostCI.p7b -Name 'HostCI-2026'
```

## Register a host key host
```powershell
Set-HgsClientHostKey                                            # on host (or -Thumbprint for your own certificate)
Get-HgsClientHostKey -Path hv01-hostkey.cer                    # on host
Add-HgsAttestationHostKey -Name hv01 -Path hv01-hostkey.cer            # on HGS
```

## Point hosts at HGS
```powershell
Set-HgsClientConfiguration -AttestationServerUrl 'http://hgs.fabric.example/Attestation' `
  -KeyProtectionServerUrl 'http://hgs.fabric.example/KeyProtection'
Get-HgsClientConfiguration     # IsHostGuarded should be True; use Get-HgsTrace if not
```

## Gotchas
- If you use a signed code integrity policy, register an unsigned copy with HGS (the signature is not measured into the TPM).
- Updates to unsigned executables need a new CI policy; use Publisher with fallback to Hash level for most signed software.

## Verify
`Get-HgsClientConfiguration` reports `IsHostGuarded` True on every guarded host, and a shielded VM starts on each.

## Checked

Checked 2026-10-26 against MicrosoftDocs/windowsserverdocs guarded-fabric pages (latest commit 2026-10-23). Wrong in the earlier draft: `Initialize-HgsAttestation` does not exist (HGS is initialised with `Initialize-HgsServer ... -TrustTpm` or `-TrustHostKey`); the pass condition is `IsHostGuarded` True (the `AttestationStatus: Passed` field is not in the page); "AD-trusted" is named admin-trusted in Microsoft's docs; TPM mode needs UEFI 2.3.1 with Secure Boot plus IOMMU/SLAT. The firmware-baseline advice was not in the cited pages and was replaced with the documented CI policy guidance. Confirmed: `Get-PlatformIdentifier`, `Add-HgsAttestationTpmHost`, `Add-HgsAttestationTpmPolicy`, `Add-HgsAttestationCIPolicy`, `Set-HgsClientHostKey`, `Get-HgsClientHostKey`, `Add-HgsAttestationHostKey` (as shown in the host-key page), `Set-HgsClientConfiguration` URLs.

Method: documentation only; no commands were run.

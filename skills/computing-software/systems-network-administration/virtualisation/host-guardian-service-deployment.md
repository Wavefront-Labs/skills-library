---
id: computing-software.systems-network-administration.virtualisation.host-guardian-service-deployment
name: host-guardian-service-deployment
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [shielded-vm, guarded-fabric, host-guardian-service, hgs, attestation, key-protection, hyper-v, windows-server]
level: sme
status: docs-checked
description: "Deploy a Host Guardian Service cluster for Hyper-V shielded VMs: HGS install, attestation mode, key protection certificates and registering guarded hosts."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-deploying-hgs-overview
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-and-shielded-vms
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-initialize-hgs-key-mode-default
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying the Host Guardian Service (HGS)

**Goal:** a guarded fabric where shielded VMs only run on Hyper-V hosts that HGS has attested as healthy,
protecting VMs from fabric administrators.

## Architecture
- **HGS**: typically a cluster of three nodes (three physical servers if you want a physical cluster) providing the
  **Attestation** and **Key Protection** services. By default `Install-HgsServer` creates a new dedicated Active
  Directory forest for it; other options are a bastion forest or an existing domain.
- **Guarded hosts**: Hyper-V hosts with the Host Guardian Hyper-V Support feature that request keys to start
  shielded VMs.
- **Shielded VMs**: generation 2 VMs with a virtual TPM, BitLocker encryption, and certain integration components
  blocked (for example data exchange and PowerShell Direct); console connections are never permitted.

## Deploy HGS (first node)
```powershell
Install-WindowsFeature -Name HostGuardianServiceRole -IncludeManagementTools -Restart
Install-HgsServer -HgsDomainName 'hgs.example' -SafeModeAdministratorPassword $dsrm -Restart
# After reboot, initialise with encryption and signing certificates (PFX from a PKI, or self-signed for labs)
Initialize-HgsServer -HgsServiceName 'hgs' -EncryptionCertificatePath enc.pfx -EncryptionCertificatePassword $p `
  -SigningCertificatePath sign.pfx -SigningCertificatePassword $p -TrustTpm   # or -TrustHostKey
```
Add nodes with `Install-HgsServer -HgsDomainName ... -HgsDomainCredential ...` followed by
`Initialize-HgsServer -HgsServerIPAddress <first-node>`.

## Attestation modes
| Mode | Trust basis | Notes |
|---|---|---|
| TPM-trusted | TPM identity, Measured Boot sequence and code integrity policy | Recommended: strongest; needs TPM 2.0 and UEFI 2.3.1 with Secure Boot; more configuration |
| Host key | Host key registered with HGS | Simpler, for hosts without TPM 2.0; similar host identification to the deprecated admin-trusted mode |
Admin-trusted (AD) attestation is deprecated from Windows Server 2019.

## Register guarded hosts
- Install the feature on the host: `Install-WindowsFeature Hyper-V, HostGuardian -IncludeManagementTools -Restart`.
- Host key: on the host `Set-HgsClientHostKey`, export the public key with `Get-HgsClientHostKey -Path <file>.cer`,
  then `Add-HgsAttestationHostKey -Name <host> -Path <file>.cer` on HGS.
- TPM: collect the identifier with `Get-PlatformIdentifier`, add it with `Add-HgsAttestationTpmHost`; capture the
  baseline (`Get-HgsAttestationBaselinePolicy`) and add it with `Add-HgsAttestationTpmPolicy`; add the code
  integrity policy with `Add-HgsAttestationCiPolicy`.
- Point the host at HGS: `Set-HgsClientConfiguration -AttestationServerUrl http://<hgs-fqdn>/Attestation
  -KeyProtectionServerUrl http://<hgs-fqdn>/KeyProtection`, then `Get-HgsClientConfiguration` must show
  `IsHostGuarded` True.

## Gotchas
- HGS is a hard dependency for starting shielded VMs: cluster it and back up its state and certificates.
- Firmware or BIOS updates change TPM baselines: register new baselines before patching hosts.
- Use HTTPS for HGS endpoints in production (the docs describe configuring HGS with HTTPS certificates).

## Verify
`Get-HgsTrace -RunDiagnostics` on a host passes; `Get-HgsClientConfiguration` shows `IsHostGuarded` True; a test
shielded VM starts on a guarded host.

## Checked

Date checked: 2026-10-27. Documentation: guarded fabric deployment, host key mode, and "Manage the Host Guardian Service" pages (windowsserverdocs main branch); Install-HgsServer, Initialize-HgsServer, Set-HgsClientConfiguration and Get-HgsTrace reference (Windows Server 2025 docset).
Confirmed: three-node cluster typical; HostGuardianServiceRole and HostGuardian feature names; Install-HgsServer and Initialize-HgsServer parameters including -TrustTpm and -TrustHostKey; attestation mode table and TPM 2.0/UEFI 2.3.1 requirements; AD mode deprecated from 2019; host key and TPM registration cmdlets; shielded VM properties; IsHostGuarded check.

Method: documentation only; no commands were run.

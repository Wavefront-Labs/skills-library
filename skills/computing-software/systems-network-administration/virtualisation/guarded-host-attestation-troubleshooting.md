---
id: computing-software.systems-network-administration.virtualisation.guarded-host-attestation-troubleshooting
name: guarded-host-attestation-troubleshooting
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [attestation-troubleshooting, get-hgsclientconfiguration, guarded-fabric, shielded-vm, host-guardian-service, hyper-v]
level: advanced
status: docs-checked
description: "Troubleshoot guarded host attestation failures so shielded VMs can start: Get-HgsClientConfiguration status and substatus, Get-HgsTrace, baseline and CI policy mismatches."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/virtualization/troubleshoot-guarded-hosts
  - https://learn.microsoft.com/en-us/powershell/module/hgsdiagnostics/get-hgstrace
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-manage-hgs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Guarded host attestation troubleshooting

Shielded VMs only start on hosts that pass attestation with the Host Guardian Service (HGS). A host that fails
attestation cannot run shielded VMs; the typical symptom is the Host Guardian Service client failing to unwrap a
key protector when the VM starts.

## Check the host
First confirm the **Host Guardian Hyper-V Support** feature (`HostGuardian`) is installed:
```powershell
Get-WindowsFeature HostGuardian
Get-HgsClientConfiguration
```
`IsHostGuarded` must be True. `Get-HgsClientConfiguration` also reports `AttestationStatus` and, when the status is
InsecureHostConfiguration, `AttestationSubStatus`.

| AttestationStatus | Meaning |
|---|---|
| Passed | host passed attestation |
| Expired | health certificate expired: check host and HGS time sync |
| InsecureHostConfiguration | host did not meet HGS policies: read the substatus |
| NotConfigured | client is in local mode: set the HGS URLs with `Set-HgsClientConfiguration` |
| TransientError | last attempt failed due to a network, service or other temporary error: retry |
| TpmError | the host could not complete attestation because of a TPM error: check TPM logs |
| UnauthorizedHost | the host is not authorised to run shielded VMs: confirm it is registered with HGS |
| Unknown | the host has not tried to attest yet |

| AttestationSubStatus | Meaning and fix |
|---|---|
| `SecureBootSettings` | TPM baseline does not match any baseline HGS trusts (new hardware or software changed Secure Boot policy): capture a new TPM baseline and register it |
| `TcgLogVerification` | the TCG log (baseline) cannot be obtained or verified: check firmware, TPM and outdated PXE boot programs |
| `CodeIntegrityPolicy` | no code integrity policy, or one HGS does not trust: configure it, restart, register it with HGS |
| `HypervisorEnforcedCodeIntegrityPolicy` | hypervisor-enforced code integrity not enabled |
| `SecureBoot` | Secure Boot is off or not using the Microsoft Secure Boot template |
| `Iommu` | VBS not configured to require an IOMMU, or no IOMMU present or enabled |
| `VirtualSecureMode` | virtualization-based security is not running |
| `BitLocker` | OS volume not BitLocker encrypted (or disable the BitLocker policy on HGS) |
| `DumpsEnabled` / `DumpEncryption` / `DumpEncryptionKey` | crash or live dumps enabled without encryption, or encrypted with a certificate HGS does not know |
| `HibernationEnabled` | hibernation allowed without an encrypted hibernation file |
| `PagefileEncryption` | page file encryption off: `fsutil behavior set encryptpagingfile 1` |
| `FullBoot` | host resumed from sleep or hibernation: restart for a clean boot |

## Automated diagnostics
```powershell
Get-HgsTrace -RunDiagnostics -Detailed                     # on the host
Get-HgsTrace -RunDiagnostics -Target $VMhost,$Server       # include other fabric nodes
```
`Get-HgsTrace` collects traces and runs diagnostics for the guarded fabric; `-Target` takes the hosts and servers
to include and `-Path` sets the output folder.

## On HGS
```powershell
Get-HgsAttestationPolicy
Get-HgsAttestationHostGroup
Get-HgsServer
```
Register new baselines and policies with `Add-HgsAttestationTpmPolicy` and `Add-HgsAttestationCiPolicy`, and new
TPM identifiers with `Add-HgsAttestationTpmHost`; host keys use `Add-HgsAttestationHostKey`.

## Gotchas
- Every firmware update can change TPM measurements in TPM mode: register the new baseline **before** rolling
  updates through the fabric.
- Admin-trusted (AD) attestation is deprecated from Windows Server 2019; host key attestation is the simpler
  alternative to TPM mode.
- If TLS 1.0 is disabled on the host, a .NET default can break HGS key unwrapping; see the Modern TLS section of
  the guarded hosts troubleshooting article.

## Verify
`Get-HgsClientConfiguration` shows `IsHostGuarded` True and AttestationStatus Passed; a shielded test VM starts.

## Checked

Date checked: 2026-10-27. Documentation: "Troubleshoot guarded hosts" (SupportArticles-docs, applies to all supported Windows Server versions), Get-HgsTrace and Get-HgsClientConfiguration reference (Windows Server 2025 docset), guarded fabric "Manage the Host Guardian Service" page.
Confirmed: HostGuardian feature name; AttestationStatus and AttestationSubStatus value tables and fixes; IsHostGuarded; Get-HgsTrace -RunDiagnostics, -Detailed, -Target and -Path; Add-HgsAttestation cmdlets and Get-HgsAttestationPolicy, Get-HgsAttestationHostGroup, Get-HgsServer; AD-mode deprecation from Windows Server 2019.

Method: documentation only; no commands were run.

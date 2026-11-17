---
id: computing-software.systems-network-administration.virtualisation.host-guardian-service-backup-and-dr
name: host-guardian-service-backup-and-dr
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hgs-backup, host-guardian-service, shielded-vms, disaster-recovery, hyper-v]
level: advanced
status: docs-checked
description: "Back up and recover the Host Guardian Service: export HGS state, protect key protection certificates, rebuild HGS from a backup and configure fallback URLs on hosts."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-manage-hgs
  - https://learn.microsoft.com/en-us/powershell/module/hgsserver/export-hgsserverstate
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-manage-branch-office
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HGS backup and disaster recovery

**Goal:** shielded VMs remain startable after losing the HGS cluster or a site.

## What must be backed up
- **HGS state**: attestation policies, trusted host groups, code integrity policies, TPM baselines and TPM
  identifiers, plus the key protection certificates that are PFX based.
- Non-exportable software certificates and HSM-held keys: ask your certificate authority or HSM vendor for a
  backup or the ability to reissue them.
A complete backup contains sensitive key material: store it securely, separately from the hosts, and keep the
certificate backups alongside the attestation-policy backups so both can be restored together.

## Export state
```powershell
$pw = Read-Host -AsSecureString -Prompt 'Export password'
Export-HgsServerState -Path .\hgs-state.xml -Password $pw
```
`Export-HgsServerState` backs up PFX-based certificates added to HGS at the time it runs.

## Restore or build DR
1. Set up a new HGS cluster per the deployment guide and install and initialise the first node
   (`Initialize-HgsServer`), using your existing keys or temporary keys. The new cluster does not need the same
   certificates, service name or domain as the original.
2. Import the backup, which restores trusted host groups, code integrity policies, TPM baselines and TPM
   identifiers; the state replicates to other HGS nodes automatically:
```powershell
Import-HgsServerState -Path .\hgs-state.xml -Password $pw
```
`-ImportActiveDirectoryModeState` or `-ImportTpmModeState` imports only one mode's policies.
Install the latest cumulative update on Windows Server 2016 before importing, or the import can fail.

## Hosts: fallback URLs
Hosts on Windows Server version 1709 or Windows Server 2019 and later can be given a fallback HGS:
```powershell
Set-HgsClientConfiguration -AttestationServerUrl 'https://hgs.contoso.com/Attestation' `
  -KeyProtectionServerUrl 'https://hgs.contoso.com/KeyProtection' `
  -FallbackAttestationServerUrl 'https://hgs-dr.contoso.com/Attestation' `
  -FallbackKeyProtectionServerUrl 'https://hgs-dr.contoso.com/KeyProtection'
Get-HgsClientConfiguration
```
Omit both fallback parameters to remove the fallback. For a host to pass attestation with both servers, keep the
attestation information up to date on both HGS clusters.

## Gotchas
- Take new backups after policy changes (new hosts, new TPM baselines, code integrity policy updates); Microsoft
  advises regular backups so the information stays current.

## Verify
Restore into an isolated lab periodically: a guarded test host attests against the restored HGS and starts a
shielded test VM.

## Checked

Date checked: 2026-10-27. Documentation: guarded fabric "Manage the Host Guardian Service" and "Manage branch office" pages (windowsserverdocs main branch), Export-HgsServerState, Import-HgsServerState and Set-HgsClientConfiguration reference (Windows Server 2025 docset).
Confirmed: what Export-HgsServerState covers (PFX-based certificates); restore procedure and that the new cluster need not reuse certificates, service name or domain; Import-HgsServerState mode switches; Windows Server 2016 cumulative-update caveat; fallback URL parameters, the 1709/2019 version gate and removal by omitting the parameters.

Method: documentation only; no commands were run.

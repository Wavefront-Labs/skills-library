---
id: computing-software.systems-network-administration.virtualisation.powercli-install-and-connect-viserver
name: powercli-install-and-connect-viserver
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [connect-viserver, powercli-install, powercli, vsphere-automation, certificates, vmware, vsphere]
level: practitioner
status: draft
description: "Install PowerCLI online or offline, handle certificate and CEIP settings, connect to one or many vCenters with stored credentials, and avoid default-server traps."
sources:
  - https://developer.broadcom.com/powercli
  - https://www.powershellgallery.com/packages/VMware.PowerCLI
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Installing PowerCLI and connecting

## Install
```powershell
Install-Module VMware.PowerCLI -Scope CurrentUser        # PS 5.1 or PS 7.x
Update-Module VMware.PowerCLI
Get-Module VMware.* -ListAvailable | Select Name, Version
```
Offline: on an internet machine `Save-Module VMware.PowerCLI -Path <SHARE>\psmodules`, copy
the folders into a path in `$env:PSModulePath` on the target, then `Get-Module -ListAvailable`.
Remove old side-by-side versions if commands misbehave (`Uninstall-Module VMware.PowerCLI -AllVersions`).

## One-time configuration
```powershell
Set-PowerCLIConfiguration -Scope User -ParticipateInCEIP $false -Confirm:$false
Set-PowerCLIConfiguration -Scope User -InvalidCertificateAction Fail      # production
# lab only: -InvalidCertificateAction Ignore
Set-PowerCLIConfiguration -Scope User -DefaultVIServerMode Single         # avoid accidental multi-vCenter ops
```
Better than Ignore: trust the VMCA root on the admin workstation (download from
`https://vcenter/certs/download.zip`, import into Trusted Root).

## Connect
```powershell
$cred = Get-Credential
Connect-VIServer vc01.corp.example -Credential $cred
# store credential (DPAPI, per-user, per-machine)
New-VICredentialStoreItem -Host vc01.corp.example -User svc-auto@vsphere.local -Password '...'
Connect-VIServer vc01.corp.example            # picks stored item
Connect-VIServer vc01, vc02 -Credential $cred -AllLinked   # Enhanced Linked Mode group
$global:DefaultVIServers                      # what you're connected to
Disconnect-VIServer * -Confirm:$false
```
For scheduled scripts prefer a vault (SecretManagement module) over the credential store.

## Gotchas
- In **Multiple** mode, `Get-VM` queries all connected servers; destructive scripts can hit
  the wrong vCenter. Pass `-Server $vc` explicitly in automation.
- Session timeout ~30 min idle; long scripts should reconnect on failure.
- PowerShell 7 + Linux needs no extra deps except for Image Builder (needs Python).
- Connecting directly to an ESXi host gives host-level cmdlets only (no DRS, tags).

## Verify
`Get-VMHost | Select Name, ConnectionState, Version` returns expected hosts; certificate
warning absent with InvalidCertificateAction Fail.

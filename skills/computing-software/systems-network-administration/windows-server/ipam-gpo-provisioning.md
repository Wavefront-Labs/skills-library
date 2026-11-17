---
id: computing-software.systems-network-administration.windows-server.ipam-gpo-provisioning
name: ipam-gpo-provisioning
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ipam, ip-address-management, invoke-ipamgpoprovisioning, ipam-provisioning, ipam-gpos, ipam-database, windows-internal-database, sql-server]
level: practitioner
status: docs-checked
description: "Install Windows Server IPAM and provision managed servers with GPOs: Invoke-IpamGpoProvisioning, database choice (WID/SQL), and the three IPAM GPOs per domain."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/invoke-ipamgpoprovisioning
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/invoke-ipamserverprovisioning
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/ipam/manage-resources-in-multiple-active-directory-forests
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# IPAM install and GPO provisioning

**What:** IPAM discovers and manages Microsoft DHCP, DNS and DC/NPS servers, tracks address
space and audits IP usage. It is agentless; servers grant it access through GPOs.

## Install
- Dedicated domain-member server (not a DC). To manage other forests, each needs a two-way trust with the forest where IPAM is installed.
```powershell
Install-WindowsFeature IPAM -IncludeManagementTools
```
Server Manager > IPAM > Provision the IPAM server (`Invoke-IpamServerProvisioning` does the same: configures WCF/WSMan settings, creates and connects to the IPAM database, creates the data collection tasks and default access-control roles): database **WID** or **SQL Server**, provisioning method **Group Policy based**, GPO prefix (e.g. `IPAM`).

## Create the GPOs (run as Domain Admin)
```powershell
Invoke-IpamGpoProvisioning -Domain ad.example.com -GpoPrefixName IPAM -IpamServerFqdn ipam01.ad.example.com -DelegatedGpoUser 'AD\ipam-admin'
```
Creates and links three GPOs with an **empty security filter list** initially:
`IPAM_DHCP`, `IPAM_DNS`, `IPAM_DC_NPS` (prefix + `_DHCP`, `_DNS`, `_DC_NPS`). They propagate the access settings the IPAM data collection tasks need, for the universal group `IPAMUG`, which the cmdlet creates and which contains the IPAM server's computer account. By default the GPOs are created on the PDC emulator (`-DomainController` overrides).

When you set a server's **Manageability status = Managed** in IPAM, IPAM adds that server to
the matching GPO's security filtering. Then on the server run `gpupdate /force`
(or wait), and refresh IPAM access status.

## Gotchas
- Access status "Blocked": the server is not Managed yet (so not in the GPO security filter list) or the GPO has not applied; run `gpupdate /force` on the server.
- The `-GpoPrefixName` must equal the prefix configured in the provisioning wizard.

## Verify
- [ ] `Get-IpamServerInventory` lists the DCs, DHCP and DNS servers with ManageabilityStatus Managed and access Unblocked in the console.
- [ ] `gpresult /r /scope computer` on a DHCP server lists `IPAM_DHCP`.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs (IPAM articles) and windows-powershell-docs (Windows Server 2025 IpamServer module) repositories, latest commit 2026-10-23. Confirmed: Invoke-IpamGpoProvisioning behaviour (three GPOs and suffixes, IPAMUG group, empty security filter list and automatic filter updates, PDC emulator default, `-DelegatedGpoUser`, `-DomainController`); Invoke-IpamServerProvisioning steps (WCF/WSMan, database, tasks, default roles); two-way trust requirement for other forests. Removed the dedicated-server and multi-domain 2016+ statement, the firewall/registry/share list, the do-not-edit advice and the remark about development status, which the checked pages do not state.

Method: documentation only; no commands were run.

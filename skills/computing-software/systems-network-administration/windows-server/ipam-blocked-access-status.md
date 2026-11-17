---
id: computing-software.systems-network-administration.windows-server.ipam-blocked-access-status
name: ipam-blocked-access-status
category: computing-software
field: systems-network-administration
product: windows-server
tags: [ipam, ipam-access-status, ipam-provisioning, invoke-ipamgpoprovisioning, ipam-discovery]
level: practitioner
status: docs-checked
description: "Fix IPAM managed servers stuck at Blocked or Unblocked-but-failing: GPO provisioning, security groups, event log and DHCP/DNS rights and firewall."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/invoke-ipamgpoprovisioning
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/get-ipamserverinventory
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/ipam/ipam-top
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# IPAM server access status Blocked

IPAM's data collection tasks reach each managed server with the IPAM server's computer account. "Blocked" access status means
those access settings are not in place.

## GPO-based provisioning checklist
1. `Invoke-IpamGpoProvisioning -Domain corp.example.com -GpoPrefixName IPAM -IpamServerFqdn ipam01.corp.example.com`
   creates and links the `IPAM_DHCP`, `IPAM_DNS` and `IPAM_DC_NPS` GPOs with an empty security filter list. The prefix must match the one used in the IPAM provisioning wizard.
2. Set the server's **Manageability Status = Managed** in the IPAM server inventory. IPAM then adds the server to the GPO's
   security filter list (unmanaged servers are removed). Until then the GPO does not apply.
3. On the managed server run `gpupdate /force` (or wait), then refresh the server access status in the console.

## What the GPOs grant
- Access settings for the IPAM server's computer account, which is what the Network Service account presents when the data collection tasks reach remote servers.
- The cmdlet creates the universal group `IPAMUG` in the domain, adds the IPAM server's computer account to it, and the GPOs propagate access settings for that group.
- It also modifies the domain-wide DNS ACL to enable DNS RPC access for `IPAMUG`.

## Still blocked?
```powershell
Get-IpamServerInventory
gpresult /r /scope:computer     # on the managed server: IPAM_* GPO applied?
Test-NetConnection dhcp01 -Port 135
```
- Check that the target server is in the GPO's security filter list (it is added only when its manageability status is Managed) and that the IPAM server's computer account is in `IPAMUG`.

## Verify
- [ ] Access status Unblocked for each managed server; data collection tasks complete.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs (IPAM articles) and windows-powershell-docs (Windows Server 2025 IpamServer module) repositories, latest commit 2026-10-23. Confirmed: Invoke-IpamGpoProvisioning: three GPOs with suffixes _DHCP, _DNS and _DC_NPS, prefix matching the provisioning wizard, empty security filter at creation and add/remove on manageability status change, universal group IPAMUG, DNS ACL change, Network Service computer-account behaviour. Removed the Event Log Readers/DHCP Users membership, firewall rule list, IPAM-server reboot advice, Domain Controllers OU remark and the `AccessStatus` column, which the checked pages do not state.

Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.windows-server.ipam-role-based-access-control
name: ipam-role-based-access-control
category: computing-software
field: systems-network-administration
product: windows-server
tags: [ipam, ipam-rbac, delegation-of-control, windows-dhcp-server, windows-dns-server]
level: practitioner
status: docs-checked
description: "Delegate IPAM with role-based access: built-in roles, custom roles and access scopes so teams manage only their DHCP scopes, DNS zones or address blocks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/ipam/role-based-access-control
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/ipam/manage-role-based-access-control-with-windows-powershell
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/ipam/create-an-access-policy
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/ipam/view-roles-and-role-permissions
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/set-ipamaccessscope
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# IPAM role-based access control

IPAM RBAC (Windows Server 2016 documentation) = **role** (what operations) + **access scope** (on which objects) + **user/group**, combined in an **access policy**. It can restrict users to specific DNS servers, zones, record types or individual resource records.

## Built-in roles
The provisioning step creates default user roles. View them and their permitted operations in the IPAM console: ACCESS CONTROL > Roles. Creating a custom role and an access policy (a user or group plus a built-in or custom role) is done in the same console area. Membership of the **IPAM Administrators** group (or local Administrators) is needed for administrative tasks such as purging data.

## Access scopes
Access scopes form a hierarchy starting at `\Global` (for example `\Global\Dublin`); create them in the console. The IpamServer module reads and sets the scope of existing objects with `Set-IpamAccessScope`, which can set a specific `-AccessScopePath` or make the object inherit with `-IsInheritedAccessScope`. Supported objects: DHCP scope, server and superscope, DNS conditional forwarder, resource records, server and zone, IP address block, range, space and subnet.
```powershell
$a = Get-IpamDnsZone -ZoneType Forward -ZoneName dublin.contoso.com
Set-IpamAccessScope -IpamDnsZone -InputObject $a -AccessScopePath '\Global\Europe' -PassThru
```
The `Get-Ipam*` cmdlets that return the objects: `Get-IpamDnsServer`, `Get-IpamDnsZone`, `Get-IpamDnsResourceRecord`, `Get-IpamDnsConditionalForwarder`, `Get-IpamDhcpServer`, `Get-IpamDhcpSuperscope`, `Get-IpamDhcpScope`.

## Custom role and assignment
In the console: ACCESS CONTROL > Roles to create a role; ACCESS CONTROL > Access Policies > Add Access Policy, choose the user or group (Locations > name), then New > select role > Add Setting > OK.

## Gotchas
- Objects can inherit the access scope from their parent (`-IsInheritedAccessScope`) or hold an explicit one; check after adding a new server.
- Changes made directly on the DHCP/DNS server are outside IPAM RBAC.

## Verify
- [ ] A test user can edit objects only inside their access scope.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs (IPAM articles) and windows-powershell-docs (Windows Server 2025 IpamServer module) repositories, latest commit 2026-10-23. Confirmed: RBAC article (restrict by DNS server, zone, record type or record); View Roles and Create an Access Policy procedures; Set-IpamAccessScope syntax, `-IsInheritedAccessScope` and the supported object list, with the dublin.contoso.com example; the Get-Ipam* object cmdlets. Replaced `Add-IpamAccessScope`, `Add-IpamRole`, `Add-IpamAccessPolicy` and `Get-IpamAccessPolicy`, which do not exist in the IpamServer module, with the console procedures; removed the built-in role list and local group names, which the checked pages do not state.

Method: documentation only; no commands were run.

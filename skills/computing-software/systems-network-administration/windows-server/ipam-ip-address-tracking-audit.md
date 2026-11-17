---
id: computing-software.systems-network-administration.windows-server.ipam-ip-address-tracking-audit
name: ipam-ip-address-tracking-audit
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ipam, ip-address-management, ipam-audit, ip-address-tracking, dhcp-lease-audit, user-logon-events, forensics, rbac-ipam, configuration-audit]
level: practitioner
status: docs-checked
description: "Use IPAM auditing: track who had an IP at a time (by IP, MAC, user or host), configuration change audit for DHCP/IPAM, and IPAM role-based access."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/get-ipamipaddressauditevent
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/remove-ipamipaddressauditevent
  - https://learn.microsoft.com/en-us/powershell/module/ipamserver/get-ipamconfigurationevent
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/ipam/manage-ipam
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# IPAM IP address tracking and audit

## IP address tracking (forensics)
IPAM correlates DHCP lease events on managed DHCP servers with user and computer authentication events on managed domain controllers and NPS servers. Search the correlated events by IP address, client ID, host name or user name.

PowerShell (IpamServer module):
```powershell
Get-IpamIpAddressAuditEvent -StartDate '<START>' -EndDate '<END>' -IpAddress 10.20.30.77
```
Parameters: `-IpAddress`, `-ClientId`, `-HostName`, `-UserName`, `-StartDate`, `-EndDate`, `-CorrelateLogonEvents`. The data returned includes both the start and end dates, and at most the top 10,000 rows are returned (with a warning); narrow the search to avoid truncation.

## Configuration audit
`Get-IpamDhcpConfigurationEvent` and `Get-IpamConfigurationEvent` return DHCP configuration events and IPAM configuration events, useful for finding who changed a scope option or IPAM data.

## Retention
Audit data lives in the IPAM database. Remove old IP address audit events with `Remove-IpamIpAddressAuditEvent -EndDate`, which permanently removes all such events up to and including that date; `Remove-IpamConfigurationEvent` and `Remove-IpamDhcpConfigurationEvent` do the same for configuration events.

## Access
Tracking data includes user names, so restrict who can see it. Roles, access policies and access scopes are managed in the IPAM console (ACCESS CONTROL); see the IPAM role-based access control skill.

## Verify
- [ ] A tracking search for a known lease returns host, MAC and user.
- [ ] Access to tracking data is limited to the audit group.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs (IPAM articles) and windows-powershell-docs (Windows Server 2025 IpamServer module) repositories, latest commit 2026-10-23. Confirmed: Get-IpamIpAddressAuditEvent description (DHCP lease correlation with DC and NPS authentication events, search keys, date inclusivity, 10,000-row cap) and parameters; Remove-IpamIpAddressAuditEvent semantics; existence of the configuration-event cmdlets. Removed the console navigation path, the logon event IDs, the WID purge advice and the built-in role names for audit access, which the checked pages do not state.

Method: documentation only; no commands were run.

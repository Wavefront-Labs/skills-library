---
id: computing-software.systems-network-administration.windows-server.directaccess-to-always-on-vpn-migration
name: directaccess-to-always-on-vpn-migration
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, remote-access, directaccess-migration, always-on-vpn, directaccess, rras]
level: advanced
status: docs-checked
description: "Plan and run the move from DirectAccess (deprecated) to Always On VPN: side-by-side deployment, client cutover, GPO removal and decommissioning the DA servers."
sources:
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-access/da-always-on-vpn-migration/da-always-on-migration-overview
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-access/da-always-on-vpn-migration/da-always-on-migration-planning
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-access/da-always-on-vpn-migration/da-always-on-migration-deploy
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-access/overview-always-on-vpn
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DirectAccess to Always On VPN migration

Always On VPN (AOVPN) is Microsoft's documented replacement for DirectAccess: it is available in all Windows editions, supports
domain-joined, workgroup and Entra ID-joined devices, and the docs describe migrating side by side in phases.

## Plan
- Build AOVPN infrastructure side by side with DirectAccess (VPN Users, VPN Servers and NPS Servers groups; certificate templates; server certificates; Remote Access for AOVPN; NPS; DNS and firewall rules; see
  always-on-vpn-infrastructure).
- Build migration rings: pilot with IT, then business users, then leadership; do not migrate a whole department in one phase; keep one VPN Users group.
- Decide device tunnel (machine, pre-logon) plus user tunnel.

## Side-by-side cutover (per client)
1. Publish the VPN user certificate template and enable autoenrollment by GPO; add migrating users to the VPN Users group.
2. Deploy the VPN profile (`VPN_Profile.ps1` or Intune) only to users who already hold the certificate: the docs use a script (`GetUsersWithCert.ps1`) that
   adds users with a non-revoked certificate from the template to a "VPN Deployment Ready" group, so the client does not try to connect without it.
3. As users migrate successfully, remove their devices from the DirectAccess security group (check Configuration Manager or Intune reporting first); never delete the DA group while it still has members.
4. Confirm AOVPN connects on and off the corporate network and that DA client settings are gone from the device.

## Decommission
- When the DirectAccess security group is empty: remove the DA configuration settings and DNS records, then remove the Remote Access role in Server Manager or
  decommission the server and remove it from AD DS.
- Remove DA-specific certificates and firewall or NAT rules you created for it.

## Gotchas
- Do tasks in order: the docs warn that performing migration steps out of order creates race conditions.
- Devices that have not yet checked in keep their DA settings; keep DA running until the DA security group is empty.

## Verify
- [ ] The DirectAccess security group is empty and monitoring shows no DA connections before shutdown.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main, windows-powershell-docs (winserver2025-ps RemoteAccess, NetNat, NetTCPIP), azure-docs vpn-gateway articles, SupportArticles-docs (troubleshoot-always-on-vpn, ms.date 2026-02-12).
Confirmed from da-always-on-vpn-migration overview, planning (migration rings) and deploy pages (side-by-side tasks, certificate-before-profile ordering, GetUsersWithCert.ps1 and the VPN Deployment Ready group)
and the includes for removing devices from the DirectAccess security group and decommissioning the server; overview-always-on-vpn (all editions, join types).
Removed the 'DirectAccess is deprecated' wording, the Get-DnsClientNrptPolicy, netsh httpstunnel and Uninstall-RemoteAccess commands, the 30-day zero-client rule and the NRPT and NLS statements, which the pages do not state.
Method: documentation only; no commands were run.

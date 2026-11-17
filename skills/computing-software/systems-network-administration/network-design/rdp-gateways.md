---
id: computing-software.systems-network-administration.network-design.rdp-gateways
name: rdp-gateways
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, access-management, rd-gateway, remote-desktop, rdp-security, bastion]
level: practitioner
status: gated
description: "Publish RDP safely through Remote Desktop Gateway or cloud bastions instead of exposing 3389: RD Gateway roles, CAP/RAP policies, MFA, UDP transport and firewall ports."
sources:
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/remote-desktop-gateway-role
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/rds-plan-mfa
  - https://learn.microsoft.com/en-us/azure/bastion/bastion-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDP gateways

Never expose TCP/UDP 3389 to the internet: it is one of the most attacked services (brute force, ransomware entry).

## Remote Desktop Gateway (Windows Server)
- Tunnels RDP inside HTTPS: clients connect on **TCP 443** (plus optional **UDP 3391** for UDP
  transport); the gateway connects internally to hosts on 3389 (gated: unconfirmed, source is paywalled or blocked).
- Policies:
  - **RD CAP** (connection authorisation): which users/groups may use the gateway, device
    redirection limits.
  - **RD RAP** (resource authorisation): which internal hosts/groups they may reach.
- Certificate from a public CA matching the external name.
- MFA via NPS extension for Microsoft Entra MFA or third-party RADIUS MFA.
- Place in DMZ or behind a reverse proxy/WAF that supports RD Gateway.

## Alternatives
- Azure Bastion (RDP/SSH over TLS from the Azure portal or a native client) or the managed bastion of other clouds.
- VPN or ZTNA client, then RDP internally.

## Hardening internally
NLA required, restrict 3389 on hosts to gateway/bastion source IPs via Windows Firewall GPO,
account lockout, Restricted Admin/Remote Credential Guard for admins.

## Verify
- [ ] External scan shows no 3389; gateway logs show MFA'd connections only to RAP-allowed hosts.

## Checked

- Date: 2026-10-28
- Confirmed: Azure Bastion overview: RDP/SSH over TLS from the portal or native client. RDS MFA article: RD Gateway as entry point, NPS with the NPS extension for Microsoft Entra MFA.
- Removed: BlueKeep, Entra application proxy/Private Access, WebSocket detail, Fleet Manager, IAP, Guacamole, gateway event log name.
- Gated: the gateway ports (TCP 443, UDP 3391) and CAP/RAP wording (the RD Gateway role page returned almost no text).
Method: documentation only; no commands were run.

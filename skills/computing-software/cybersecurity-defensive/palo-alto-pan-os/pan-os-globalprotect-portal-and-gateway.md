---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-globalprotect-portal-and-gateway
name: pan-os-globalprotect-portal-and-gateway
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [globalprotect-gateway, pan-os, globalprotect, portal, remote-access-vpn, agent-config, split-tunnel]
level: practitioner
status: draft
description: "Configure a GlobalProtect portal and gateway on PAN-OS with authentication, tunnel interface, agent config and split tunnel."
sources: ["https://docs.paloaltonetworks.com/globalprotect/11-1/globalprotect-admin/globalprotect-portals/globalprotect-portal-configuration"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: remote users connect and receive an IP, DNS and routes.

Pieces
1. Server certificate (public CA) and SSL/TLS service profile.
2. Authentication profile (see authentication-profile skill; SAML plus MFA recommended).
3. A tunnel interface in a `vpn-users` zone with a dedicated routed subnet.
4. Gateway (Network > GlobalProtect > Gateways): interface, certificate, authentication, tunnel settings (IP pool), network services (DNS, WINS) and split-tunnel include/exclude routes.
5. Portal: interface, certificate, authentication, agent config (external gateways, connect method, app settings), and a trusted root CA for the agent.
6. Security policy from `vpn-users` to internal zones and NAT if needed.

```
show global-protect-gateway current-user
show global-protect-gateway statistics
show global-protect-portal statistics
less mp-log gpsvc.log
```
(Log file names confirm per release.)

Gotchas
- Pre-logon (machine certificate) and always-on connect methods need certificates and a user-ID plan.
- Split tunnel by app or domain (confirm licence/release) lets you keep SaaS off the tunnel.
- Overlapping client IP pool and a remote LAN breaks routing; plan address space.
- User-ID for tunnel users comes from GlobalProtect login events, so enable User-ID on the vpn zone.

## Verify
Connect a test client; `show global-protect-gateway current-user` lists the user with assigned IP, and the GlobalProtect logs show the login with the matching config.

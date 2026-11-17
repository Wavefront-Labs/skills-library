---
id: computing-software.networking-hardware-and-wireless.check-point.remote-access-vpn-and-mobile-access
name: remote-access-vpn-and-mobile-access
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, remote-access-vpn, mobile-access, endpoint-vpn-client]
level: practitioner
status: draft
description: "Enable Check Point Remote Access VPN with office mode, authentication and the Mobile Access portal."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_RemoteAccessVPN_AdminGuide/Default.htm
  - https://www.checkpoint.com/training/certification/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Remote Access VPN and Mobile Access

- Enable **IPsec VPN** (for the Remote Access client) and/or **Mobile Access** (SSL portal, Capsule/Endpoint clients) on the gateway. Create a **Remote Access community** (the built-in `RemoteAccess`), add the gateway and the user groups allowed.
- **Office Mode** gives clients addresses from a pool (Network object or DHCP) so internal servers can return traffic; add the pool to routing and to anti-spoofing on the internal interface.
```
mgmt_cli -r true add user-group name "VPN_Users"
mgmt_cli -r true add access-rule layer "Network" position top name "RA VPN" source "VPN_Users@Any" destination "Internal_Nets" vpn "RemoteAccess" action "Accept" track.type "Log"
```
- Authentication: user passwords (internal), AD/LDAP, RADIUS or certificates; add MFA via RADIUS. Specify the authentication order in the gateway object > VPN Clients > Authentication.
- The client downloads the **site topology** from the gateway; changing the topology needs a policy install and a client site update.
- Mobile Access portal listens on 443; if the gateway already serves the management/UserCheck web on 443, set a unique port or IP (multi-portal main URL).
- Gotcha: split tunnelling versus "route all" is set in **Remote Access > Office Mode / Traffic flow**; users reaching the internet through the tunnel need the internal gateway to hide-NAT the Office Mode pool.

Verify: connect with a client; `vpn tu` and the Logs `VPN` shows the user; `fw tab -t userc_users -s`/`vpn overlap_encdom` for domain overlaps (confirm).

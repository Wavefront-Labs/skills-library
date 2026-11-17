---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-8021x-eap-design
name: wifi-8021x-eap-design
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-8021x, eap-tls, radius-wlan]
level: advanced
status: draft
description: "Design 802.1X wireless authentication: EAP type choice, RADIUS redundancy, certificate trust and client supplicant settings."
sources:
  - https://www.wi-fi.org/
  - https://www.rfc-editor.org/rfc/rfc5216
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 802.1X for WLAN

- Roles: supplicant (client) - authenticator (AP/controller) - authentication server (RADIUS). The AP relays EAP; keys derive from the EAP method (PMK).
- Prefer EAP-TLS (mutual certificates) for managed devices; PEAP-MSCHAPv2 is common but depends on password strength and correct server-certificate validation on clients.
- Clients must validate the RADIUS server certificate (pin the CA and server name) or they can be tricked by a rogue AP with a lookalike SSID.
- Run at least two RADIUS servers; set sensible timeouts and failover on the controller. Use Fast Roaming (see roaming skills) so reauthentication does not stall voice clients.
- Dynamic VLAN or role assignment by RADIUS attributes lets one SSID serve multiple groups.
- WPA3-Enterprise 192-bit mode requires EAP-TLS with suites such as GCMP-256; confirm client support.

## Verify
- [ ] RADIUS logs show EAP-TLS success and expected VLAN/role attributes.
- [ ] A test client with a wrong CA does not connect.

---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-secure-management-plane
name: nda-secure-management-plane
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [management-plane-hardening, ssh-only-management, management-vrf, nda-access-aaa]
level: practitioner
status: draft
description: "Lock down device management with SSH keys, no telnet/HTTP, management ACLs and a dedicated management VRF or out-of-band network."
sources:
  - https://www.cisco.com/
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Management-plane hardening

- Disable telnet and plain HTTP; use SSHv2 (key-based where supported) and HTTPS with valid certificates.
- Restrict access: ACL or firewall filter on VTY lines/management interface to the management network; a management VRF/instance separates it from user traffic.
- Out-of-band management (console server, dedicated management port) keeps access when the data path is broken.
- Disable unused services (HTTP server, CDP/LLDP on edge ports where not needed, SNMPv1/v2c).
- Logging banner, session timeouts, and login rate limiting.

## Verify
- [ ] An external scan of the management IPs shows only SSH/HTTPS reachable from the management network.

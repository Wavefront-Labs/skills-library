---
id: computing-software.systems-network-administration.netbird.ports-and-firewalls
name: ports-and-firewalls
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, firewall-rules, stun-ports, relay-ports, ufw-wt0, static-wireguard-port]
level: practitioner
status: docs-checked
description: "NetBird Cloud firewall requirements: outbound-only rules for management, signal, STUN and relay, TLS inspection exemptions, host firewall fixes and static peer ports."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/about-netbird/ports-and-firewalls.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
No inbound ports are needed; peers connect outbound and hole-punch via ICE/STUN.

Outbound for NetBird Cloud:
- Management and Signal: `api.netbird.io`, `signal.netbird.io`, TCP/443.
- STUN: `stun.netbird.io`, UDP 80, 443, 3478, 5555 (recommended for direct connections; IPs are dynamic, and nftables pins IPs at load time so reload periodically).
- Relay: `relay.netbird.io` and `*.relay.netbird.io`, TCP/443 (WebSocket) and UDP/443 (QUIC). Clients v0.36.0+ use whichever connects first.
- Legacy TURN (clients before v0.29.0 only): `turn.netbird.io`, UDP 80 and 443, TCP 443-65535.

Exempt NetBird domains from TLS inspection and DPI; list `relay.netbird.io` and `*.relay.netbird.io` explicitly since `*.netbird.io` may not match. Peers staying relayed can mean per-destination NAT: use port-preserving NAT and a longer UDP timeout.

Site-to-site static ports: `netbird up --wireguard-port <port>` from a reserved range, preserve source port at the main-site NAT, UDP timeout about 240 seconds or more. Avoid for roaming laptops.

Host firewalls: NetBird manages `wt0` rules itself; conflicts come from other tools. UFW: `sudo ufw allow in on wt0`. firewalld: add `wt0` to the trusted zone and reload. Windows: confirm the NetBird rule and check Group Policy or security software; on flat networks without NAT add an inbound UDP 49152-65535 rule scoped to `netbird.exe`.

Diagnostics: `netbird debug bundle --system-info`, plus `iptables -L -n -v`, `nft list ruleset`, `ufw status verbose` on Linux.

## Checked

2026-11-04: read the Ports and Firewalls page in full. Confirmed the outbound endpoints and ports, the STUN nftables caveat, relay transports and v0.36.0, the legacy TURN range, TLS inspection exemptions, per-destination NAT note, static port procedure, host firewall fixes, the flat-network Windows rule and the diagnostics commands. Nothing removed.

Method: documentation only; no commands were run.

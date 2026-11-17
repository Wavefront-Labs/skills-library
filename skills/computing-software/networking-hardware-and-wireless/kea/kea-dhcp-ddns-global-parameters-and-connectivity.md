---
id: computing-software.networking-hardware-and-wireless.kea.kea-dhcp-ddns-global-parameters-and-connectivity
name: kea-dhcp-ddns-global-parameters-and-connectivity
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp-ddns, d2, dhcp-ddns, max-queue-size, ncr-protocol]
level: practitioner
status: docs-checked
description: "Configure where D2 listens and how kea-dhcp4 or kea-dhcp6 reach it: DhcpDdns ip-address and port, the dhcp-ddns block, queue size, and control socket."
sources:
  - https://kea.readthedocs.io/en/latest/arm/ddns.html
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D2 global parameters and DHCP server connectivity
D2 side (`DhcpDdns`):
- `ip-address`: default 127.0.0.1 (IPv4 or IPv6).
- `port`: default 53001.
- `dns-server-timeout`: milliseconds to wait for a DNS server per update message; default 500.
- `ncr-protocol` (only UDP) and `ncr-format` (only JSON).

Anything other than loopback should be for testing only: an attacker could send bogus NCRs, and local users can still reach D2. If address or port change, change the DHCP servers' `dhcp-ddns` section to match.

DHCP server side (`Dhcp4/dhcp-ddns`, same for DHCPv6):
- `enable-updates` (connectivity switch) and `ddns-send-updates` (behaviour) must both be true for requests to be generated.
- `server-ip` (default 127.0.0.1) and `server-port` (53001).
- `sender-ip` (blank lets Kea choose) and `sender-port` (0 lets Kea choose).
- `max-queue-size`: default 1024. When the queue of unsent requests reaches it, DDNS updating is turned off until the backlog drops, so lease operations continue without unbounded memory growth.

```json
"Dhcp4": { "dhcp-ddns": { "server-ip": "192.168.1.10", "server-port": 900 } }
```

A control socket for D2 is opened only if `control-sockets` is configured.

## Checked
2026-11-04. Confirmed against the Kea Administrator Reference Manual (The DHCP-DDNS Server chapter and the DHCPv4 DDNS section). Removed: nothing.
Method: documentation only; no commands were run.

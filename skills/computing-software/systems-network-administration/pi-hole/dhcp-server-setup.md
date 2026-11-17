---
id: computing-software.systems-network-administration.pi-hole.dhcp-server-setup
name: dhcp-server-setup
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-dhcp-server, dhcp-range, lease-time]
level: practitioner
status: docs-checked
description: "Enable and configure Pi-hole's built-in DHCP server: address pool, gateway, netmask, lease time, IPv6 and logging."
sources: ["https://docs.pi-hole.net/ftldns/configfile/", "https://docs.pi-hole.net/main/post-install/", "https://docs.pi-hole.net/docker/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pi-hole DHCP server

Disable DHCP on your router before enabling Pi-hole's DHCP server, otherwise two servers answer. The server is off by default (`dhcp.active = false`).

**Core options**

| Option | Meaning |
| --- | --- |
| `dhcp.start` / `dhcp.end` | First and last address of the pool, such as `192.168.0.10` to `192.168.0.250` |
| `dhcp.router` | Gateway address, typically your router |
| `dhcp.netmask` | Optional for directly connected networks, determined from the interface; give it explicitly for networks reached via a relay, otherwise Pi-hole guesses from the address class |
| `dhcp.leaseTime` | Seconds, or `45m`, `1h`, `2d`, `1w`, or `infinite` (with drawbacks); default is one hour for IPv4 and one day for IPv6 |
| `dhcp.ipv6` | Also satisfy IPv6 address requests (default `false`) |
| `dhcp.rapidCommit` | DHCPv4 Rapid Commit (RFC 4039); only enable if this is the only server for the subnet |
| `dhcp.multiDNS` | Advertise the Pi-hole DNS multiple times to stop devices adding their own DNS servers |
| `dhcp.logging` | Log DHCP activity to the dnsmasq log (`files.log.dnsmasq`) for debugging |

Docker needs host networking, macvlan or a relay (see the Docker DHCP skill) plus `NET_ADMIN`.

**Checklist**

1. Turn off router DHCP.
2. Set pool, router and lease time.
3. Enable `dhcp.active`.
4. Renew a client lease and confirm the client gets an address from the pool.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: FTL Configuration Reference (ftldns/configfile); Post-Install (main/post-install); Docker Configuration (docker/configuration). Reworded the unconfirmed check step about the Settings page.
Method: documentation only; no commands were run.

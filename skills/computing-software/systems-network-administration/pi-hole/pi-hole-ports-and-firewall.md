---
id: computing-software.systems-network-administration.pi-hole.pi-hole-ports-and-firewall
name: pi-hole-ports-and-firewall
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-ports, pihole-firewall, ufw-rules]
level: practitioner
status: docs-checked
description: "Open the right TCP/UDP ports for DNS, web, DHCP and NTP on a Pi-hole host while limiting access to the local network."
sources: ["https://docs.pi-hole.net/main/prerequisites/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pi-hole ports and firewall rules

`pihole-FTL` uses these ports:

| Service | Port | Protocol |
| --- | --- | --- |
| DNS | 53 | TCP/UDP |
| DHCP (optional) | 67 | IPv4 UDP |
| DHCPv6 (optional) | 547 | IPv6 UDP |
| Web/API | 80 and 443 | TCP |
| NTP server (optional) | 123 | UDP |

If another web server already holds 80 or 443, FTL tries 8080 or 8443. If neither is free, the web interface is unavailable until you set `webserver.port`.

Pi-hole is designed for a local network, so restrict sources. Typical private ranges are `192.168.0.0/16`, `10.0.0.0/8` and `172.16.0.0/12`; check your own before applying rules.

**iptables example (IPv4)**

```bash
iptables -I INPUT 1 -s 192.168.0.0/16 -p tcp -m tcp --dport 80 -j ACCEPT
iptables -I INPUT 1 -s 192.168.0.0/16 -p udp -m udp --dport 53 -j ACCEPT
```

**firewalld**

```bash
firewall-cmd --permanent --add-service=http --add-service=https --add-service=dns --add-service=dhcp --add-service=dhcpv6 --add-service=ntp
firewall-cmd --reload
```

**ufw** stores rules persistently: `ufw allow 53/tcp`, `ufw allow 53/udp`, `ufw allow 80/tcp`, `ufw allow 443/tcp`, plus `ufw allow 546:547/udp` for IPv6 DHCP.

The page marks 67, 547 (DHCP) and 123 (NTP) as optional features that need additional ports; its iptables, ufw and firewalld examples are guides only, so use your distribution's documentation for the exact commands.

## Checked

2026-11-03. Read the Prerequisites page: the port table, the 8080/8443 fallback, the private ranges, and the iptables, firewalld and ufw examples (the iptables lines shown are copied from it; the page also lists more rules, including 53 for 127.0.0.0/8 and DHCP/NTP).

Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.network-design.layered-osi-troubleshooting-and-tcp-vs-udp
name: layered-osi-troubleshooting-and-tcp-vs-udp
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, osi-model, encapsulation, layered-troubleshooting, tcp-vs-udp, pdu, bottom-up, top-down, connectivity-checklist, transport-layer, troubleshooting-methodology]
level: intro
status: docs-checked
description: "Use the OSI/TCP-IP layers as a troubleshooting checklist: what to test at each layer and with which command, and how TCP vs UDP behaviour changes the symptoms you see."
sources:
  - https://www.comptia.org/certifications/network
  - https://datatracker.ietf.org/doc/html/rfc1122
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Layered troubleshooting and TCP vs UDP

## A layer-by-layer checklist
| Layer | PDU | Question | Test |
|---|---|---|---|
| 1 Physical | bits | link light, errors? | `ethtool <interface>` (Linux), interface error counters, cable tester |
| 2 Data link | frame | right VLAN, MAC learned, no STP block? | the switch's MAC address table, `ip neigh show` |
| 3 Network | packet | address/mask/gateway right, route both ways? | `ip route`, then ping the gateway and the remote host, and traceroute |
| 4 Transport | segment/datagram | port open, firewall allows, SYN answered? | `Test-NetConnection <host> -Port 443` (Windows), `ss -tlnp` (Linux listeners) |
| 5-7 Application | data | name resolves, TLS valid, app responds? | a DNS lookup, `openssl s_client -connect host:443`, `curl -v` |
Bottom-up for "nothing works"; top-down when one app fails and others work; divide-and-conquer
(start at layer 3 with a ping) when unsure.

## Encapsulation reminder
Application data -> TCP/UDP header (ports) -> IP header (addresses, TTL, DF) -> Ethernet header
(MACs, VLAN tag) + FCS. Each device acts up to its layer: switches read L2, routers rewrite L2
and decrement TTL, firewalls/load balancers read L4-7.

## TCP vs UDP: what changes in troubleshooting
| | TCP | UDP |
|---|---|---|
| Connection | 3-way handshake; failure is visible (RST or SYN timeout) | none; no reply may be normal |
| Closed port | RST from host | ICMP port unreachable (often filtered: looks like a timeout) |
| Firewall drop | SYN retransmits then timeout | silence |
| Loss | retransmitted; shows as slowness | lost data; app-level retry or glitches (voice) |
| Testing | a TCP connect test such as `Test-NetConnection -Port` | a port check cannot prove a UDP service works; use the service's own client |
| NAT/firewall state | per-device idle timeout | per-device idle timeout, often shorter: check it when a long-idle UDP flow breaks |
Look up each protocol's transport in its RFC or vendor documentation before choosing the test.

## Verify
- [ ] The fault is localised to one layer with a concrete failing test and a passing test below it.
- [ ] For UDP services, testing used a real protocol client rather than a port check.

## Checked

2026-10-28: Confirmed: RFC 1122 (host sends ICMP Port Unreachable when UDP cannot be demultiplexed; TCP uses RST for the equivalent), ss flags -t -l -n -p (man7), Test-NetConnection -Port (Microsoft Learn), ip neigh show (man7), openssl s_client -connect, curl --verbose and ethtool devname. Removed: the 30-120 s and hours NAT timeout figures, nc/telnet/arp/dig/ntpdate/snmpget test commands and the protocol-to-transport list, none of which a fetched page supported.
Method: documentation only; no commands were run.

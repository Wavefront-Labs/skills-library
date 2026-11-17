---
id: computing-software.firmware-embedded-development.iot-protocols.thread-border-router
name: thread-border-router
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [thread-border-router, thread-network, thread, border-router, otbr, rcp, iot-protocols]
level: practitioner
status: docs-checked
description: "Thread Border Router: minimum functions, OpenThread Border Router (OTBR) with an RCP, NAT64, prefix delegation and firewall rules."
sources:
  - https://openthread.io/guides/border-router
  - https://www.threadgroup.org/What-is-Thread/Overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread Border Router

**Goal:** Connect a Thread network to Wi-Fi or Ethernet.

## Steps
1. A Thread network needs a Border Router to reach other networks. Minimum functions: two-way IP connectivity, two-way DNS-based service discovery (mDNS on the Wi-Fi/Ethernet side, SRP on the Thread side), Thread-over-infrastructure to merge partitions across IP links, and external commissioning (for example from a phone).
2. OpenThread Border Router (OTBR) supports the Radio Co-Processor design: the 802.15.4 chip runs only sub-MAC and PHY, and the rest of OpenThread runs on the host.
3. OTBR features: NAT64 to reach IPv4 networks, DHCPv6 Prefix Delegation to obtain IPv6 prefixes, and a Thread Border Agent for external commissioning.
4. OTBR services: an mDNS Publisher so an external commissioner can find the OTBR and its network, and a PSKc Generator.
5. OTBR ingress filtering uses iptables and ipset. It blocks inbound packets with on-link source addresses (OMR or Mesh-Local prefix), inbound unicast not destined to an OMR or Domain Unicast Address, and inbound unicast with link-local source or destination.

## Gotcha
Do not treat OTBR as a transparent bridge: the firewall drops inbound unicast that is not addressed to an OMR or Domain Unicast Address, so a LAN ping to a mesh-local address will not work.

## Verify
- [ ] LAN host reaches a Thread node on its OMR (global) address
- [ ] The OTBR is discoverable by mDNS from an external commissioner
- [ ] Ping to a mesh-local or link-local address from outside is blocked, as designed

## Checked

2026-11-08. Confirmed on the OpenThread border router page: minimum functions, RCP design, NAT64, DHCPv6-PD, Border Agent, mDNS Publisher, PSKc Generator and the three ingress filter rules. Removed as unsupported by the cited pages: DNS64, SRP server and advertising proxy details, multiple-border-router election, the _meshcop._udp service name, ecosystem examples (HomePod, Nest Hub) and the dataset-mismatch partition claim. Verify steps rewritten to match the firewall behaviour. The Thread Group page does not mention border routers.
Method: documentation only; no commands were run.

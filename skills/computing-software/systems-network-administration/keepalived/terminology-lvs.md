---
id: computing-software.systems-network-administration.keepalived.terminology-lvs
name: terminology-lvs
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, terminology, lvs, vip, real-server, server-pool, virtual-service]
level: intro
status: docs-checked
description: "Keepalived LVS vocabulary: VIP, real server, server pool, virtual server, virtual service, WAN and LAN interfaces."
sources:
  - https://keepalived.readthedocs.io/en/latest/terminology.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LVS terminology

- **LVS:** Linux Virtual Server, a kernel feature adding load balancing, working as a NAT-style bridge for TCP/UDP streams.
- **WAN interface:** the NIC clients use to reach the balancer.
- **LAN interface:** the NIC used to manage the load-balanced servers.
- **VIP:** the address clients connect to; they never reach real servers directly.
- **Real server:** a host running the application that serves requests.
- **Server pool:** a group of real servers.
- **Virtual server:** the access point to a pool.
- **Virtual service:** a TCP/UDP service tied to the VIP.

The page leaves RIP, DIP, Director and IPVS undefined (to-do).

## Checked

2026-11-04: terms confirmed against the Terminology page (LVS and LVS Component sections). Removed the generic Verify line.
Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.virtual-ips-and-maglev-hashing
name: virtual-ips-and-maglev-hashing
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [virtual-ip, maglev-hashing, consistent-hashing, ecmp, network-load-balancer, ipvs, katran, load-balancing]
level: advanced
status: docs-checked
description: "How VIP load balancing works per the SRE Book: connection tracking vs hashing, consistent hashing, direct server response, and GRE encapsulation with its MTU cost; Maglev context."
sources: ["https://sre.google/sre-book/load-balancing-frontend/", "https://sre.google/workbook/managing-load/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual IPs and Maglev hashing

SRE Book "Load Balancing at the Frontend": a virtual IP (VIP) is not assigned to one network interface but shared
across many devices, while remaining a single regular IP address to the user. This hides the number of machines
behind a VIP and eases upgrades and capacity changes. The key device is the network load balancer, which receives
packets and forwards them to a backend.

## The connection-affinity problem
- **Least-loaded backend** looks ideal but breaks for stateful protocols: the balancer must track every connection
  so later packets reach the same backend.
- **Stateless hash**: derive a connection ID from the packet, e.g. `id(packet) mod N` for N backends. No state, and
  every packet of a connection goes to one backend. But when a backend is removed, N becomes N-1 and almost every
  packet maps to a different backend, resetting almost all connections if backends share no state.
- **Consistent hashing** (proposed in 1997) stays relatively stable when backends are added or removed, minimising
  disruption. The book's practice: usually use simple connection tracking, and fall back to consistent hashing
  when the system is under pressure (for example during a denial-of-service attack).

## Maglev in the Workbook
Maglev is Google's custom distributed packet-level load balancer. Packets for a given IP address can be spread
evenly over a pool of Maglev machines with Equal-Cost Multi-Path (ECMP) forwarding, so capacity grows by adding
machines and redundancy can be modelled as N+1 rather than the active/passive 1+1 pairs of traditional balancers.
For the lookup-table algorithm itself, read the Maglev paper (not checked here).

## Forwarding to backends
- **NAT** needs an entry per connection in the tracking table, which precludes a stateless fallback.
- **Direct Server Response (DSR)**: change the destination MAC address at layer 2, so the backend sees the original
  IPs and replies directly to the sender. Large savings when requests are small and replies large, and no state
  on the balancer. The drawback: all balancers and backends must reach each other at the data link layer, in one
  broadcast domain, which Google outgrew.
- **Encapsulation**: the balancer wraps the packet in another IP packet using Generic Routing Encapsulation (GRE),
  addressed to the backend; the backend strips the outer layer. Balancer and backend need no shared broadcast
  domain. The cost is inflated packets (24 bytes for IPv4+GRE), which can exceed the MTU and need fragmentation;
  a larger MTU inside the datacenter avoids it if the network supports it.

## Gotchas
- Encapsulation without MTU handling causes problems on large packets.
- Drain a backend before removing it rather than relying on the hash alone.

## Verify
- [ ] Removing one backend resets only its connections (measure resets during a drain test).
- [ ] MTU/MSS validated end to end with large payloads.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Load Balancing at the Frontend" (VIP definition, id(packet) mod N, consistent hashing from 1997, connection tracking with hashing fallback, NAT, DSR, GRE encapsulation, 24 bytes IPv4+GRE, MTU) and the SRE Workbook "Managing Load" (Maglev, ECMP, N+1).
Removed: the Maglev table construction description and Python sketch, prime table size, Katran, IPVS `mh`, Envoy policy, the `ipvsadm` command and kernel version, the 1/N remap figure, and their sources (not read).
Method: documentation only; no commands were run.

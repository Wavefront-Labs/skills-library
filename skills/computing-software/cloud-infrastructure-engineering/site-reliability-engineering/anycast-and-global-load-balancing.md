---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.anycast-and-global-load-balancing
name: anycast-and-global-load-balancing
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, load-balancing, anycast-load-balancing, global-load-balancing, bgp, geodns]
level: advanced
status: docs-checked
description: "Global traffic distribution with DNS and anycast: what the SRE Book says about DNS limits, VIPs and consistent hashing, plus RFC 4786 anycast operating practice."
sources: ["https://sre.google/sre-book/load-balancing-frontend/", "https://datatracker.ietf.org/doc/html/rfc4786"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anycast and global load balancing

**Goal:** send each user to a nearby, healthy and non-overloaded site, and survive site failures.

## DNS load balancing (SRE Book, Load Balancing at the Frontend)
- "Optimal" depends on the traffic: a search request goes to the nearest available datacenter by RTT for latency; a
  video upload may take a less loaded path to maximise throughput.
- Returning several A/AAAA records gives little control: the client picks arbitrarily and each attracts roughly equal
  traffic. SRV weights and priorities are not adopted for HTTP.
- Clients cannot find the closest address themselves. Mitigations: an anycast address for the authoritative
  nameservers so queries reach the nearest one, or a map of networks to physical locations (more complex, needs a
  pipeline to keep it current).
- The recursive resolver sits between users and the authoritative server, so the server sees the resolver's address,
  not the user's. The EDNS0 client-subnet extension passes the user's subnet. One nameserver may also serve users
  across a wide area (the book's example is an ISP resolving from one datacenter).
- Resolvers cache within TTL, so one reply may reach one user or thousands, and TTL sets a lower bound on how fast
  changes propagate (not all resolvers respect TTL). The DNS balancer should also account for capacity and the health
  of the selected datacenter, by integrating with global control systems.
- A DNS reply must fit the 512-byte limit of RFC 1035 in the book's account, bounding the number of addresses.
  DNS is the simplest and most effective first layer but not sufficient alone.

## Virtual IPs and the network load balancer (SRE Book)
- A VIP is shared across many devices; a network load balancer forwards packets to a backend.
- Least-loaded selection needs per-connection tracking for stateful protocols. Hashing a connection ID with `id mod N`
  needs no state but remaps almost every connection when one backend is removed. Consistent hashing keeps the mapping
  stable when the backend set changes; the book uses simple connection tracking normally and falls back to consistent
  hashing under pressure such as a DoS attack.
- Forwarding options: NAT (needs per-connection state), layer 2 MAC rewriting with direct server response (all machines
  must share a broadcast domain, which the book says Google outgrew), and GRE packet encapsulation (backends need not
  share a broadcast domain). Encapsulation adds overhead (24 bytes for IPv4+GRE) that can exceed the MTU.

## Anycast operation (RFC 4786, BCP)
- Withdraw on failure: couple the route advertisement to service health, so a failing service triggers a route
  withdrawal. This can be done by running routing protocol software on the same server as the service.
- Avoid rapid advertise/withdraw oscillation, for example by a minimum delay after a withdrawal before re-advertising.
  Frequent flaps can exhaust router CPU remotely, so BGP implementations dampen them; dampening elsewhere can make a
  node unreachable. Mitigations in the RFC: stable Global Nodes plus Local Nodes, and aggressive dampening close to the
  origin.
- TCP caveat: with equal-cost paths to different anycast nodes, packets of one transaction may reach more than one
  node, and TCP involves multiple packets (the handshake). Per-packet load balancing is described as pathological for
  this use; with BGP, equal-cost paths are normally not a concern.
- Scope: Global Nodes advertise routes globally; Local Nodes limit propagation (for example NO_EXPORT or NOPEER
  communities, or peering rather than transit import policy) and should use policy that requires explicit attributes
  to propagate. Accidental propagation beyond the intended horizon can overload Local Nodes. Combining Global and Local
  Nodes also reduces cascading failure risk, since failover is generally from Local to Global.

## Verify
- [ ] A drain test withdraws one site and traffic shifts to the others without overloading them.
- [ ] Withdrawal is health-driven with a re-advertisement delay.
- [ ] DNS TTLs and resolver behaviour are accounted for in the failover time estimate.

## Checked

Checked 2026-11-09. Confirmed against the SRE Book Load Balancing at the Frontend chapter and RFC 4786 (withdrawal on
failure, oscillation, dampening, equal-cost paths and TCP, Local and Global Nodes). Removed: the Cloudflare and Google
Cloud documentation sources (not read), the comparison table of GeoDNS, anycast and managed edge products, the /24 prefix
rule, ExaBGP/BIRD tooling, the claim that failover converges in seconds to minutes, AS-path prepend traffic engineering, the
N+2 across sites sizing rule and the per-site monitoring list, none of which appeared on the pages read.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.

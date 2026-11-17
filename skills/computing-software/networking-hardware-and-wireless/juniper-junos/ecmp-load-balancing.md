---
id: computing-software.networking-hardware-and-wireless.juniper-junos.ecmp-load-balancing
name: ecmp-load-balancing
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, load-balance, ecmp, per-packet, multipath]
level: practitioner
status: draft
description: "Enable equal-cost multipath on Junos with a load-balance per-packet policy (really per-flow) and BGP multipath."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ECMP and load-balance policy
Goal: use multiple equal-cost paths.

```
set policy-options policy-statement LB then load-balance per-packet
set routing-options forwarding-table export LB
set protocols bgp group PEERS multipath
set protocols bgp group PEERS multipath multiple-as
set forwarding-options hash-key family inet layer-3
set forwarding-options hash-key family inet layer-4
```

```
user@host> show route 10.20.0.0/16 exact
user@host> show route forwarding-table destination 10.20.0.1
```

- Despite the name `per-packet`, Junos hashes per flow; by default a route keeps one next-hop even with multiple equal paths until this policy is applied.
- BGP needs `multipath` to install more than one equal path.
- Hash fields vary by platform: confirm.

Gotcha: policy applied only to the routing table export, not the forwarding table, does nothing. It must be under `routing-options forwarding-table export`.

Operational tip: hash polarisation can occur when successive tiers hash on the same fields; vary hash seeds or fields per tier where the platform allows, and check balance with interface counters.

## Verify
- The forwarding table entry shows `ulst` (unilist) with multiple next-hops.

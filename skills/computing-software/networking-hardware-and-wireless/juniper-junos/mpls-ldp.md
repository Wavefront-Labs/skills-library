---
id: computing-software.networking-hardware-and-wireless.juniper-junos.mpls-ldp
name: mpls-ldp
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, mpls, ldp, label-switching, lsp]
level: practitioner
status: draft
description: "Enable Junos MPLS with LDP over an IGP and verify labels and LSPs."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MPLS and LDP basics
Goal: build an LDP-signalled label-switched core.

```
set interfaces xe-0/0/3 unit 0 family mpls
set protocols mpls interface xe-0/0/3.0
set protocols ldp interface xe-0/0/3.0
set protocols ldp interface lo0.0
set protocols ldp transport-address router-id
```

```
user@host> show ldp neighbor
user@host> show ldp session
user@host> show ldp database
user@host> show route table mpls.0
user@host> traceroute mpls ldp 10.255.0.2/32
```

- LDP follows the IGP; every loopback must be reachable in inet.0 first.
- `family mpls` must be on each core interface.
- `traffic-engineering bgp-igp` and `mpls.0` / `inet.3` interplay for next-hop resolution (confirm on your design).

Gotcha: LDP session up but no LSP to a loopback is usually due to missing /32 route or `transport-address` mismatch. RSVP-TE is separate (`protocols rsvp`).

Operational tip: enable `set protocols ldp track-igp-metric` and `ldp-synchronization` (confirm on your release) so traffic does not black-hole while LDP is still coming up after an IGP adjacency.

## Verify
- `show ldp session` is `Operational`; `show route table inet.3` has loopback entries.

---
id: computing-software.networking-hardware-and-wireless.arista-eos.static-and-ecmp
name: static-and-ecmp
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, static-routes, ecmp, ip-route, route-preference]
level: practitioner
status: draft
description: "Add EOS static routes, administrative distance, ECMP, and track next-hops with BFD."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Static routes, ECMP and route preference
Goal: simple routing with failover.

```
ip route 0.0.0.0/0 198.51.100.2
ip route 0.0.0.0/0 203.0.113.2 200
ip route 10.20.0.0/16 Null0
ip route 10.30.0.0/16 198.51.100.2 track bfd
ip route 10.40.0.0/16 198.51.100.2
ip route 10.40.0.0/16 198.51.100.4
```

```
show ip route
show ip route 10.40.0.1
show ip route summary
```

- Number at the end is the administrative distance (default 1).
- Two equal-cost routes create ECMP; the hash defaults to L3/L4 fields (`load-balance` options are platform specific: confirm).
- `maximum-paths` applies to dynamic routing protocols.

Gotcha: a static route pointing to an unreachable next-hop is not installed; `show ip route` simply lacks it. Use `show ip route 10.40.0.1 detail` to see why.

Operational tip: prefer dynamic routing with BFD for production paths and reserve statics for management, null routes and blackholing. Document each static with its reason in the config comment (`!`).

## Verify
- `show ip route 0.0.0.0/0` shows `S` with the expected next-hops.

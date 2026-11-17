---
id: computing-software.networking-hardware-and-wireless.frrouting.zebra-ecmp-and-nexthop-weights
name: zebra-ecmp-and-nexthop-weights
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, zebra, ecmp, multipath, nexthop-weight, resilient-nexthop-group, nexthop-group]
level: advanced
status: docs-checked
description: "FRR zebra ECMP limits, 16-bit nexthop weights, nexthop-group keep time and resilience settings, and how to inspect ECMP routes and zebra-created nexthop groups."
sources:
  - https://docs.frrouting.org/en/latest/zebra.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zebra ECMP and nexthop weights
- Default compile limit is 64-way ECMP, configurable at build time; `-e X, --ecmp X` lowers it at startup. Protocols set their own ECMP policy.
- `--nexthop-weight-16-bit` (startup) uses 16-bit instead of 8-bit weights; the dataplane must support 16-bit weighted ECMP groups. 8-bit weights scale to 1-254, 16-bit to 1-65534.
- Kernel hashing is controlled by the `fib_multipath_hash_policy` sysctl; zebra has limited control after installation.
- `zebra nexthop-group keep (1-3600)` seconds to keep an unused installed nexthop group (default 180).
- `zebra nexthop-group resilience buckets (1-256) idle-timer (1-4294967295) unbalanced-timer (1-4294967295)` makes all zebra-created multipath groups resilient; groups a protocol requests as resilient keep their own settings.

Inspect:
- `show ip route X` shows all ECMP nexthops; `*` marks FIB-installed routes. Kernel view: `ip route show X`.
- `show nexthop-group rib [ID] [vrf NAME] [singleton [ip|ip6]] [type] [json [brief]]`; "Initial Delay" means the group is deferred until used.
- `show [ip|ipv6] route ... nexthop-group summary [ecmp-count <gt|lt|eq> (1-256)]` filters by ECMP count (requires `summary`).

## Checked

2026-11-08. Read the FRR zebra page: ECMP section and 64-way default, -e/--ecmp, --nexthop-weight-16-bit and weight scaling, fib_multipath_hash_policy, zebra nexthop-group keep and resilience, show ip route and show nexthop-group rib forms. Fixed the --ecmp option spelling.
Method: docs-only read of cited pages, 2026-11-08

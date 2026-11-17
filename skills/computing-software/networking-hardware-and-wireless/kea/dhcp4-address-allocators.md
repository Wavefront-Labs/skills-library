---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-address-allocators
name: dhcp4-address-allocators
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, allocator, iterative, random, free-lease-queue, flq]
level: advanced
status: docs-checked
description: "Choose the iterative, random or free lease queue address allocator per subnet in kea-dhcp4 and know the trade-offs."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 allocators
The `allocator` parameter picks how an available address is found; it is set globally or per subnet.

- `iterative` (default): offers the last offered address plus one. Very fast at low utilization, slow at high. With several servers sharing a lease database it causes allocation conflicts and client retransmissions.
- `random`: uniform random choice; suits servers sharing a database or cluster and resists attacks based on predictable allocation. Slightly slower and uses more memory, growing with offered addresses.
- `flq` (free lease queue): keeps a running list of free addresses per pool for constant-time selection, good for highly utilized pools. Costs: slower startup and reconfiguration (a /8 pool may delay startup 15 seconds or more; a /16 or smaller should be acceptable), memory proportional to pool size, and lease reclamation must be enabled with a low `reclaim-timer-wait-time` because expired leases are not free until reclaimed.
- Shared FLQ, added in Kea 3.1.9, is experimental and not supported for production; it targets shared MySQL or PostgreSQL lease backends.

```json
"subnet4": [ { "id": 1, "subnet": "192.0.2.0/24", "allocator": "flq" } ]
```

## Checked

2026-11-08. Read dhcp4-srv.rst (Kea ARM source, master branch) sections Allocators Comparison, Iterative, Random, Free Lease Queue and Shared Free Lease Queue (partial read of the page, those sections in full). Confirmed the default, trade-offs, the /8 and /16 startup remarks, reclaim-timer-wait-time requirement, and that shared FLQ was added in Kea 3.1.9 and is experimental. Nothing removed.

Method: documentation only; no commands were run.

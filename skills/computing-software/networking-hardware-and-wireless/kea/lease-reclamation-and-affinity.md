---
id: computing-software.networking-hardware-and-wireless.kea.lease-reclamation-and-affinity
name: lease-reclamation-and-affinity
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, lease-expiration, expired-leases-processing, lease-affinity, leases-reclaim]
level: advanced
status: docs-checked
description: "Tune expired lease reclamation in Kea with expired-leases-processing timers and limits, lease affinity via hold-reclaimed-time, and leases-reclaim."
sources:
  - https://kea.readthedocs.io/en/latest/arm/lease-expiration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lease reclamation and affinity
Settings live in the `expired-leases-processing` map:
- `reclaim-timer-wait-time`: default 10 s.
- `flush-reclaimed-timer-wait-time`: default 25 s.
- `hold-reclaimed-time`: default 3600 s; non-zero enables lease affinity.
- `max-reclaim-leases`: default 100; 0 is unlimited.
- `max-reclaim-time`: default 250 ms; 0 is no limit.
- `unwarned-reclaim-cycles`: default 5.

```json
"expired-leases-processing": { "reclaim-timer-wait-time": 10,
  "hold-reclaimed-time": 1800, "max-reclaim-leases": 100 }
```

Reclamation steps: lease4_expire or lease6_expire callouts, removal of DNS entries, lease database update, then counters. The `leases-reclaim` command triggers it on demand.

If `flush-reclaimed-timer-wait-time` and `hold-reclaimed-time` are both non-zero, a client release expires the lease instead of deleting it.

## Checked
2026-11-04. Confirmed against the Kea Administrator Reference Manual (Lease Expiration chapter). Removed: nothing.
Method: documentation only; no commands were run.

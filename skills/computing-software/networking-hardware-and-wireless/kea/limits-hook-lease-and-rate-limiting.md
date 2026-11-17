---
id: computing-software.networking-hardware-and-wireless.kea.limits-hook-lease-and-rate-limiting
name: limits-hook-lease-and-rate-limiting
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, hooks, libdhcp-limits, address-limit, prefix-limit, rate-limit]
level: advanced
status: docs-checked
description: "Cap leases and packet rates per client class or subnet with libdhcp_limits using user-context limits: address-limit, prefix-limit and rate-limit."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# limits hook
Loading `libdhcp_limits.so` alone limits nothing. Add `limits` to the `user-context` of a client class, subnet or subnet inside a shared network. On reconfiguration Kea logs one line per configured limit with LIMITS_CONFIGURED in its identifier.

```json
"client-classes": [ { "name": "cable-modem-1",
  "test": "option[123].hex == 0x000C4B1E",
  "user-context": { "limits": { "address-limit": 4 } } } ]
```

Lease limits: an unsigned 32-bit integer. `address-limit` covers IPv4 and IPv6 IA_NA leases; `prefix-limit` covers IA_PD. Counts update in the lease4_select, lease4_renew, lease6_select, lease6_renew and lease6_rebind callouts, so classes with `only-in-additional-list` true cannot be lease-limited. Under load Kea may allocate slightly more than the limit.

Rate limits: `"rate-limit": "4 packets per minute"` in the form "p packets per time-unit" with second, minute, hour, day, week, month (30 days) or year (365 days). They are checked at pkt4_receive/pkt6_receive, as early as possible, so only classes assigned to the packet itself can be used. Value 0 means literally no packets are processed; it does not disable limiting. To disable, remove the `rate-limit` entry, the `limits` map, or the library. A lease limit of 0 works the same, but rate limiting strains Kea less.

## Checked
2026-11-04. Confirmed against the Kea Administrator Reference Manual (Hook Libraries chapter, libdhcp_limits.so). Removed: nothing.
Method: documentation only; no commands were run.

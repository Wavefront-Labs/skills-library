---
id: computing-software.networking-hardware-and-wireless.squid.delay-pools-classes
name: delay-pools-classes
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, delay-pools, delay-class, bandwidth-limit, traffic-shaping]
level: practitioner
status: docs-checked
description: "Enable delay pools and choose among classes 1 to 5 to group traffic for bandwidth limiting."
sources:
  - https://www.squid-cache.org/Doc/config/delay_pools/
  - https://www.squid-cache.org/Doc/config/delay_class/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delay pools and classes
`delay_pools N` sets the number of pools (default 0); Squid must be built with `--enable-delay-pools`. Then use `delay_class`, `delay_parameters` and `delay_access`. Example: one class 2 and one class 3 pool means `delay_pools 2`.

One `delay_class` line per pool:
- Class 1: one shared limit for all traffic (IPv6 works)
- Class 2: adds a per-host limit (last octet of an IPv4 address)
- Class 3: adds a subnet limit (third octet) and per-host limit
- Class 4: class 3 plus a per-user limit; needs forced authentication
- Class 5: groups by tag from an external ACL (IPv6 works)

Classes 2 to 4 use bitmasks, so IPv4 only.
```
delay_class 1 2    # pool 1 is a class 2 pool
delay_class 3 4    # pool 3 is a class 4 pool
```

## Checked

2026-11-04. Read the delay_pools and delay_class directive pages and confirmed the default, the build option, the five classes, the IPv4-only note for classes 2 to 4 and the example lines. Nothing was removed.

Method: documentation only; no commands were run.

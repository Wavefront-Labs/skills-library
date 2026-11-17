---
id: computing-software.systems-network-administration.coredns.coredns-secondary-plugin
name: coredns-secondary-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, secondary, axfr, zone-transfer, catalog]
level: advanced
status: docs-checked
description: "Act as a secondary by pulling zones via AXFR from primaries, with retry, jitter, catalog zones and fallthrough."
sources:
  - https://coredns.io/plugins/secondary/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replicate a zone from another server.

Syntax:

```
secondary [ZONES...] {
    transfer from ADDRESS [ADDRESS...]
    catalog
    fallthrough [ZONES...]
}
```

Behaviour:
- Zones are fetched by AXFR and are not written to disk, which the docs note violates the RFC. A restart refetches all secondary zones.
- If primaries do not answer at startup, AXFR is retried indefinitely every 10 seconds.
- `transfer from` can appear several times; if one address fails another is tried.
- When the refresh timer fires, a random jitter of 5 seconds is applied before fetching; on retry it is 2 seconds. Transfer errors are logged.
- `catalog` treats the transferred zone as an RFC 9432 catalog zone: after each successful catalog transfer, member zones are added or removed and transferred from the same primaries.
- `fallthrough` passes NXDOMAIN to the next plugin, optionally only for listed zones, useful in split DNS when the secondary zone holds partial records.

Example:

```
example.org {
    secondary {
        transfer from 10.0.1.1 10.1.2.1
    }
}
```

To re-serve the zone to other secondaries, enable the transfer plugin in the same block.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/secondary/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.

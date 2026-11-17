---
id: computing-software.networking-hardware-and-wireless.kea.statistics-and-stat-commands
name: statistics-and-stat-commands
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, statistics, statistic-get, statistic-reset, sample-count, monitoring]
level: practitioner
status: docs-checked
description: "Read and manage Kea statistics: value types, reset behavior, statistic-get and related commands, and sample age or count limits."
sources:
  - https://kea.readthedocs.io/en/latest/arm/stats.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea statistics and statistic commands
Statistic types: integer (64-bit), big integer (128-bit), float, duration, string.

Lifecycle: packet counters reset on restart; per-subnet statistics are recalculated on reconfiguration.

Commands:
- `statistic-get`, `statistic-get-all`, `statistic-global-get-all`
- `statistic-reset`, `statistic-reset-all`
- `statistic-remove`, `statistic-remove-all`
- `statistic-sample-age-set`, `statistic-sample-age-set-all`
- `statistic-sample-count-set`, `statistic-sample-count-set-all`

```json
{ "command": "statistic-get", "arguments": { "name": "pkt4-received" } }
```

Each statistic keeps 20 data points by default. The retention limit is either time-based (age, `duration` in seconds) or size-based (count, `max-samples`); only one type of limit is active per statistic. `statistic-reset` sets a statistic to its neutral value (0, 0.0, 0h0m0s0us or an empty string) while `statistic-remove` deletes it, though the server may add it back.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Kea ARM statistics chapter (types, lifecycle, sections 17.3.1-17.3.11, Time Series: 20 data points, one limit type). Added the reset versus remove difference and parameter names from the same chapter.

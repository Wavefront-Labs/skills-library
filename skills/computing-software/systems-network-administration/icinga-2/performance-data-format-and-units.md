---
id: computing-software.systems-network-administration.icinga-2.performance-data-format-and-units
name: performance-data-format-and-units
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, performance-data, perfdata, uom, label, metrics, normalization, lc-numeric]
level: advanced
status: docs-checked
description: "Format plugin performance data for Icinga 2: the label=value;warn;crit;min;max schema, label rules, C locale numbers, units."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/05-service-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# performance data format and units
Append metrics to the plugin output after a `|` character:
```
<output> | 'label'=value[UOM];[warn];[crit];[min];[max]
```
Label rules: wrap in single quotes; avoid spaces and special characters like `%` (they can break receivers such as Graphite); labels must not contain `'` or `=`; keep them short and unique. Multiple values are joined with a space. Values must follow the C/POSIX locale (no comma decimals); Icinga sets `LC_NUMERIC=C` on plugin execution.

`warn`, `crit`, `min` and `max` are optional, separated by `;` and share the value's unit. Docs example:
```
PING OK - Packet loss = 0%, RTA = 12.44 ms|rta=12.445000ms;100.000000;200.000000;0.000000 pl=0%;5;15;0
```
**Units.** UoMs are written as-is to the core backends (IDO, API), so 12.445000ms stays 12.445000ms. Metric backends (Graphite, InfluxDB and others) get values normalised, including warn/crit/min/max: 12.445000ms becomes 0.012445 seconds. Icinga DB receives both as-is and normalised data.

Normalised families include bytes (B to YB, KiB to YiB), bits, packets, seconds (ns, us, ms, s, m, h, d), percent (%), amperes, ohms, volts, watts and watt-hour variants, lumens (lm), dBm, grams (ng to t), degrees (C, F, K) and liters (ml, l, hl). The UoM `c` marks a continuous counter. Unknown UoMs are discarded as if none was given. A value with no UoM may be an integer or float of any type, such as processes or users.

Plugins that switch size units (MB to GB) for the same label do so to keep graphs looking the same.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/05-service-monitoring/. No commands were run.

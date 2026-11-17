---
id: computing-software.cloud-infrastructure-engineering.netdata.alert-lookup-syntax
name: alert-lookup-syntax
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, alert-lookup, percentage-of-time, anomaly-bit]
level: advanced
status: docs-checked
description: "Netdata alert lookup lines: method, time window, options, dimension lists and the percentage-of-time, flaps and times query methods with conditions."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/src/health/REFERENCE.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Syntax:

```
lookup: METHOD(GROUPING OPTIONS) AFTER [at BEFORE] [every DURATION] [OPTIONS] [of DIMENSIONS]
```

- `AFTER` is a negative duration (`-1m`, `-1h`, `-1d`); `at BEFORE` ends the window (default now).
- `of` takes a comma- or pipe-separated list, patterns allowed; write `user,system`, not `user, system`.
- Result is `$this`.

Options: `percentage`, `absolute`, `min`/`max`/`average`/`sum` (cross-dimension aggregation, `sum` default), `min2max`, `unaligned`, `anomaly-bit` (0-100), `match-ids` (default) or `match-names`.

```
lookup: average -10m unaligned of user,system,softirq,irq,guest
lookup: average -1m percentage of used
lookup: average -5m anomaly-bit of *
```

Condition-based methods: `percentage-of-samples` (alias `countif`), `percentage-of-time`, `number-of-flaps`, `number-of-times`.

```
lookup: percentage-of-time(>90) -1h
```

Operators: `>`, `>=`, `<`, `<=`, `=`, `!=` (and listed aliases). No operator means equal; omitted condition means `==0`. No `and`/`or` compounds. Gap tokens `gap`, `nan`, `null`, `empty` must be named for gaps to count in samples, flaps and times methods. `previous`/`last` compares to the previous sample.

## Checked

2026-11-04. Confirmed against the Netdata health reference: lookup parameter table, the `of` list rule, the options table with sum and match-ids defaults, the anomaly-bit 0-100 range, the three lookup examples, the four fleet-query methods and the countif alias, operator list, no-operator and omitted-condition rules, gap tokens, previous/last, and no and/or compounds. Removed the closing UNDEFINED gotcha, which the page does not state.

Method: documentation only; no commands were run.

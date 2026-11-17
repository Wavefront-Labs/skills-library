---
id: computing-software.database-administration.cockroachdb.load-based-splitting
name: load-based-splitting
category: computing-software
field: database-administration
product: cockroachdb
tags: [load-based-splitting, range-split, hotspots, qps-threshold, rebalancing]
level: practitioner
status: docs-checked
description: "Control CockroachDB load-based range splitting: enable setting, QPS threshold, split heuristics, and the 'no split key found' log message."
sources:
  - https://www.cockroachlabs.com/docs/stable/load-based-splitting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let hot ranges split automatically so load spreads across more leaseholders and nodes.

Settings:
```sql
SET CLUSTER SETTING kv.range_split.by_load_enabled = false;   -- default is enabled
SET CLUSTER SETTING kv.range_split.load_qps_threshold = 2000; -- default 2500
```
It is enabled by default; the page suggests disabling it only when troubleshooting range-related issues under the guidance of Cockroach Labs support. Lower the threshold if splitting earlier helps your workload; raise it on very large machines to split more conservatively.

How it works: once a range exceeds the QPS threshold it becomes eligible and per-key metrics are collected. A split happens only if both heuristics agree:
- Balance factor: would load be even on both sides? If 99% of traffic hits one key, splitting does little.
- Split crossing: how many queries would span the new boundary? Multi-range queries cost more, so a split can hurt.
The split point is placed at the first set of keys whose combined operations exceed the threshold. Combined with load-based rebalancing this evens load per node, rather than only evening out leaseholder counts.

Monitoring: the log message `no split key found: ...` means CockroachDB tried to split for load but could not identify a key to split at; it can usually be ignored, but if it repeats it may indicate a load imbalance, for example a range that cannot be split because of a hot key.

Verify: `SHOW CLUSTER SETTING kv.range_split.by_load_enabled;` returns `true`.

## Checked
2026-11-03. Confirmed on the load-based splitting page: enabled by default, `kv.range_split.load_qps_threshold` default 2500, lower or raise guidance, balance factor and split crossing heuristics, split point at the first set of keys exceeding the threshold, and the `no split key found` log message. Removed: the INFO level claim and the Hot Ranges verify.
Method: documentation only; no commands were run.

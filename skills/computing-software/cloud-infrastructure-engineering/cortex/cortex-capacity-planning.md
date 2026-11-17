---
id: computing-software.cloud-infrastructure-engineering.cortex.cortex-capacity-planning
name: cortex-capacity-planning
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [capacity-planning, sizing, ingester-memory, series, retention]
level: advanced
status: docs-checked
description: "Estimate Cortex sizing from active series, sample rate, churn and compressibility, and apply the ingester memory rule of thumb."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/capacity-planning.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The page itself warns it is likely out of date for blocks storage, so treat the numbers as rough.

Key inputs: number of active series (query `prometheus_tsdb_head_series` if you run Prometheus), sampling rate (samples per series per interval times series count), series churn (very high with short-lived jobs that carry unique IDs, analyse with tsdb analyze), compressibility (a constant metric over 12h of 15s samples is around 2KB; a jumpy one around 10KB, with no tool to analyse it) and retention. Also relevant at high values: series per metric name, labels per series, and query rate and complexity.

Rule of thumb: each million series in an ingester takes 15GB of RAM. The series count in ingesters is active series times the replication factor. This assumes the default 12-hour chunks; lowering `-ingester.max-chunk-age` reduces RAM at the cost of more back-end I/O.

Memory also rises during write-ahead log replay, and an ingester without enough memory for replay cannot restart without intervention. It rises temporarily during resharding too, because series briefly exist on both old and new ingesters.

## Checked

2026-11-04. Claims were read against the Cortex docs page: Capacity planning guide (see sources). Removed filler and unconfirmed wording.

Method: documentation only; no commands were run.

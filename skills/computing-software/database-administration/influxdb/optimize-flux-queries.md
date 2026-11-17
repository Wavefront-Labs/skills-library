---
id: computing-software.database-administration.influxdb.optimize-flux-queries
name: optimize-flux-queries
category: computing-software
field: database-administration
product: influxdb
tags: [flux, query-performance, pushdown, profiler, windowing]
level: advanced
status: docs-checked
description: "Speed up Flux queries: lean on pushdown functions, avoid inline computed filters, short windows and heavy transforms, and profile with the profiler package."
sources:
  - https://docs.influxdata.com/influxdb/v2/query-data/optimize-queries/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Guidance from the page:

- Start the query with pushdown-capable functions such as `range()` and `filter()` so work happens in the data source; once a non-pushdown function runs, Flux pulls data into memory. The page's table lists which functions and combinations push down; verify per function.
- Do not compute filter values inline. Compute them once: `region = v.provider + v.region`, then `filter(fn: (r) => r.region == region)`.
- Avoid very short aggregation windows.
- Heavy functions: `map`, `reduce`, `join`, `union`, `pivot`. Use them late, on reduced data.
- Prefer `set()` over `map()` to assign static values.
- Downsample for long ranges.

Profile:

```js
import "profiler"
option profiler.enabledProfilers = ["query", "operator"]
```

The `query` profiler gives statistics for the whole script and `operator` gives statistics per operation; metrics are appended to the query output. Filter pushdown only works when all parameter values are static.

## Checked

Method: docs-checked 2026-11-09 against the Optimize Flux queries page, read in full from the overview to the profilers section. The pushdown support table lost its per-version icons in the text I read, so that matrix is not claimed.

---
id: computing-software.data-engineering.polars.lazy-scan-and-collect-engines
name: lazy-scan-and-collect-engines
category: computing-software
field: data-engineering
product: polars
tags: [polars, lazy, scan-csv, collect, streaming, gpu, polars-lazy-execution, lazyframe]
level: practitioner
status: docs-checked
description: "Start a Polars lazy query with scan_* or .lazy(), then pick collect() settings: default, engine=streaming for larger-than-memory, engine=gpu, or head() for sampling."
sources:
  - https://docs.pola.rs/user-guide/lazy/using/
  - https://docs.pola.rs/user-guide/lazy/execution/
  - https://docs.pola.rs/user-guide/lazy/gpu/
  - https://docs.pola.rs/user-guide/lazy/sources_sinks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build a lazy query and run it with the right `collect` mode.

Start lazily
- From a file: `pl.scan_csv(...)` (also IPC, Parquet, JSON scans). Prefer `scan_*` over `read_*`: the optimizer pushes work into the reader so unneeded columns and rows are skipped, and streaming can process batches before the file is fully read.
- From memory: call `.lazy()` on a `DataFrame`.

```python
q1 = (
    pl.scan_csv("docs/assets/data/reddit.csv")
    .with_columns(pl.col("name").str.to_uppercase())
    .filter(pl.col("comment_karma") > 0)
)
```
Nothing runs until you collect.

Choose a collect mode
- `.collect()`: the optimized graph runs as one batch, so all data must fit in memory at peak usage.
- `.collect(engine="streaming")`: may process larger-than-memory data in batches.
- `.collect(engine="gpu")`: in-memory GPU engine (RAPIDS cuDF, NVIDIA GPUs, Python only). Open Beta; targets a single GPU (multi-GPU via GPUEngine objects, see gpu-engine-cudf-polars); needs Polars installed with the GPU feature flag.
- Partial runs while developing: scan a subset of partitions, or put `.head(10)` right after the scan and `.collect()` at the end. Aggregations and filters on a subset may not match the full-data result.

Gotchas
- A `LazyFrame` is a query plan, not a cache. Reusing it in separate downstream queries recomputes it each time. Operations that do not maintain row order (such as `group_by`) can return a different order on every run; pass `maintain_order=True` to avoid that.
- For queries that diverge from a shared base, use `pl.collect_all` (see lazy-multiplexing-collect-all).

Check: on the Reddit example the page shows `collect()` returning shape (14_029, 6) from 10 million rows, and the `.head(10)` variant returning a 1-row frame (id 6).

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). Removed or trimmed claims the cited page does not confirm.

Method: documentation only; no commands were run.

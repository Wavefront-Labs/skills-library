---
id: computing-software.data-engineering.polars.lazy-multiplexing-collect-all
name: lazy-multiplexing-collect-all
category: computing-software
field: data-engineering
product: polars
tags: [polars, lazy, collect-all, multiplexing, explain-all, cache, polars-lazy-multiplexing, lazyframe]
level: practitioner
status: docs-checked
description: "Avoid recomputing or reordering a shared LazyFrame by passing all diverging branches to pl.collect_all in one optimization pass."
sources:
  - https://docs.pola.rs/user-guide/lazy/multiplexing/
  - https://docs.pola.rs/user-guide/lazy/execution/
  - https://docs.pola.rs/user-guide/lazy/sources_sinks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: branch one LazyFrame into several outputs without re-evaluating it per branch.

The trap
An eager `df1 = df.group_by("n").len()` stores a result, so slicing it twice is consistent. A `LazyFrame` stores a query plan instead:

```python
lf1 = df.lazy().group_by("n").len()
out = [lf1.slice(offset=i * 5, length=5).collect() for i in range(2)]
pl.testing.assert_frame_equal(lf1.collect(), pl.concat(out))
```
This raises `AssertionError: DataFrames are different (value mismatch for column 'n')`, because each `collect` re-runs the group-by and group-by output order is not stable. It is also expensive.

The fix
Give Polars all plans in a single optimization and execution pass:

```python
lf1 = df.lazy().group_by("n").len()
out = [lf1.slice(offset=i * 5, length=5) for i in range(2)]
results = pl.collect_all([lf1] + out)
pl.testing.assert_frame_equal(results[0], pl.concat(results[1:]))
```
`pl.explain_all([lf1] + out)` shows the combined queries under a single "SINK_MULTIPLE" evaluation, with "CACHE" nodes marking subplans the optimizer recognised as shared.

Same pattern elsewhere
- Diverging queries: `pl.collect_all([lf_1, lf_2])` executes the shared `lf` only once.
- Multiple sinks: `q1 = lf.sink_parquet(.., lazy=True)`, `q2 = lf.sink_ipc(.., lazy=True)`, then `pl.collect_all([q1, q2])`.

Why it matters: combining related subplans in one execution unit can give large performance increases and permits diverging plans, temporary tables and a more procedural style.

Related: pass `maintain_order=True` on order-sensitive operations, as the execution page advises.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.

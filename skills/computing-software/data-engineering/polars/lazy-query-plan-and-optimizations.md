---
id: computing-software.data-engineering.polars.lazy-query-plan-and-optimizations
name: lazy-query-plan-and-optimizations
category: computing-software
field: data-engineering
product: polars
tags: [polars, lazy, explain, show-graph, query-plan, predicate-pushdown, polars-lazy-query-plan, graphviz]
level: practitioner
status: docs-checked
description: "Inspect Polars optimized and non-optimized query plans with explain and show_graph, and know which optimizations the lazy engine applies."
sources:
  - https://docs.pola.rs/user-guide/lazy/query-plan/
  - https://docs.pola.rs/user-guide/lazy/optimizations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: see what the optimizer changed in a lazy query.

Every lazy query has a non-optimized plan (steps as written) and an optimized plan.

```python
q1 = (
    pl.scan_csv("docs/assets/data/reddit.csv")
    .with_columns(pl.col("name").str.to_uppercase())
    .filter(pl.col("comment_karma") > 0)
)
q1.explain(optimized=False)        # printed, non-optimized
q1.explain()                       # printed, optimized
q1.show_graph(plan_stage="ir", optimized=False)
q1.show_graph(plan_stage="ir")     # optimized IR graph
q1.show_graph(plan_stage="physical")  # streaming engine physical plan
```
Graph output needs Graphviz installed and on PATH. The page text says the physical plan is shown with `plan_type="streaming"` (the default) when using the streaming engine, while its code uses `plan_stage="physical"`.

Reading plans
- Read both text and graph plans from bottom to top.
- In graphs: each box is a stage, sigma is SELECTION (filters), pi is PROJECTION (column subset).
- Non-optimized text: FILTER over WITH_COLUMNS over `CSV SCAN` with `PROJECT */6 COLUMNS` (wildcard = all columns).
- Optimized text: the filter moves into the scan as `SELECTION: [(col("comment_karma")) > (0)]`, applied while the CSV is read line by line. This is predicate pushdown.

Optimizations table (non-complete)
- Predicate pushdown, projection pushdown, slice pushdown, common subplan elimination, join ordering: run 1 time.
- Simplify expressions (constant folding, faster replacements) and type coercion: until fixed point.
- Cardinality estimation (picks group by strategy): 0/n times depending on the query.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). Removed or trimmed claims the cited page does not confirm.

Method: documentation only; no commands were run.

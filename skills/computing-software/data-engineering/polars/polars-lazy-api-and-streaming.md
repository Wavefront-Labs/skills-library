---
id: computing-software.data-engineering.polars.polars-lazy-api-and-streaming
name: polars-lazy-api-and-streaming
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-lazy-api, polars-streaming, scan-csv, collect, explain, predicate-pushdown, projection-pushdown, query-plan]
level: practitioner
status: docs-checked
description: "Switch from eager to lazy Polars with scan_csv and collect, read the plan with explain, and run larger-than-memory queries with engine=streaming."
sources:
  - https://docs.pola.rs/user-guide/concepts/lazy-api/
  - https://docs.pola.rs/user-guide/concepts/streaming/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lazy API, explain, and streaming

Goal: defer execution so the query planner can optimise, and run big queries in batches.

## Eager to lazy

Eager: each step runs immediately and returns intermediates (`pl.read_csv`, `filter`, `group_by`...). Lazy: build the query, then call `collect`.

```python
q = (
    pl.scan_csv("docs/assets/data/iris.csv")
    .filter(pl.col("sepal_length") > 5)
    .group_by("species")
    .agg(pl.col("sepal_width").mean())
)
df = q.collect()
```

Optimisations the docs name for this query:

- Predicate pushdown: apply filters as early as possible while reading, so only rows with sepal length greater than 5 are read.
- Projection pushdown: read only the needed columns (petal length and width are skipped).

Effect: lower memory and CPU load, so bigger datasets fit and run faster. Many eager calls actually call the lazy API under the hood and collect immediately.

## When to use which

Prefer lazy unless you need intermediate results or are exploring and do not yet know the query.

## Preview with explain

```python
print(q.explain())
```

The plan shows the pushdowns (rows filtered at the scan, only needed columns). `explain` also shows how expression expansion unfolds for a schema:

```python
schema = pl.Schema({"int_1": pl.Int16, "int_2": pl.Int32,
                    "float_1": pl.Float64, "float_2": pl.Float64, "float_3": pl.Float64})
print(pl.LazyFrame(schema=schema)
      .select((pl.col(pl.Float64) * 1.1).name.suffix("*1.1")).explain())
```

## Streaming

Pass `engine="streaming"` to `collect` to execute in batches, so datasets that do not fit in memory can be processed. The page also says the streaming engine is more performant than the in-memory engine.

```python
df = q.collect(engine="streaming")
```

- Some operations are inherently non-streaming or not implemented yet; Polars falls back to the in-memory engine for those, without you needing to know.
- To debug memory or performance, plot the physical graph: `q.show_graph(plan_stage="physical", engine="streaming")`. The legend shows how memory intensive each operation can be.
- The streaming engine can report per-node runtime metrics to Polars Nanook (a dashboard); see the Query monitoring page.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/concepts/lazy-api/; https://docs.pola.rs/user-guide/concepts/streaming/. Corrected: Removed an unverifiable source note; renamed the managed service to Polars Nanook as the monitoring page does. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.

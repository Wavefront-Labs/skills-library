---
id: computing-software.data-engineering.polars.pandas-to-polars-concepts
name: pandas-to-polars-concepts
category: computing-software
field: data-engineering
product: polars
tags: [polars-migration-pandas, pandas, migration, no-index, null-vs-nan, strict-types, lazy-evaluation, engines]
level: practitioner
status: docs-checked
description: "Conceptual differences a pandas user must internalise before writing Polars: no index, Arrow memory, parallelism, engines, laziness, strict types, nulls, expressions."
sources:
  - https://docs.pola.rs/user-guide/migration/pandas/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Think in Polars, not pandas

Goal: avoid porting pandas habits that run but run slowly or wrongly. The migration guide's one rule: `polars != pandas`; code that looks like pandas "might run, but it likely runs slower than it should".

## Concept differences

- **No index / multi-index.** Each row is addressed by integer position only. Semantics of a query should not depend on an index or a `reset_index` call. There is no `.loc`/`iloc` and no `SettingWithCopyWarning`. Resampling and similar are explicit "verb" methods naming the columns they act on. (Database-style indexes are used internally only as an optimisation.)
- **Memory:** Polars uses the Apache Arrow columnar format; pandas defaults to NumPy arrays. Convert to NumPy with `to_numpy`.
- **Parallelism:** Polars runs many operations in parallel via Rust; pandas core is single-threaded and needs a library such as Dask.
- **Engines:** a native in-memory engine, a streaming engine for large-scale data, and native integration with a cuDF-supported engine. All share the query optimizer and Polars keeps semantics consistent across them (pandas numpy/pyarrow backends can differ in dtype and semantics).
- **Lazy evaluation:** Polars supports eager and lazy; pandas only eager. Lazy mode builds a query plan and applies automatic query optimization.
- **Strictness:** dtype resolution depends on the operation graph. pandas loosely converts (new missing data turns an integer column into float); Polars keeps the integer column.
- **Missing data:** a single `null` for every dtype. Float columns may also hold `NaN`, which is a special float value, not missing data.
- **Expressions:** Polars is built on expressions accepted almost everywhere. It treats a needed Python `lambda` as a gap in its API and tries to provide native support.

## Practical rules

1. Default to lazy mode: use an implicitly lazy reader such as `scan_csv`, or call `.lazy()`, and finish with `.collect()`.
2. Replace pandas `lambda` chains with `pl.col(...)` expressions.
3. Put several column computations in one `select`/`with_columns` so they run in parallel (see pandas-to-polars-syntax-patterns).

See also: pandas-to-polars-syntax-patterns, pandas-transform-and-pipe-to-expressions.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.

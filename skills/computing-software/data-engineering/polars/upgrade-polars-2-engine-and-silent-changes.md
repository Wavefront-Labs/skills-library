---
id: computing-software.data-engineering.polars.upgrade-polars-2-engine-and-silent-changes
name: upgrade-polars-2-engine-and-silent-changes
category: computing-software
field: data-engineering
product: polars
tags: [polars-upgrade-2, upgrade, streaming-engine, engine-affinity, row-order, concat-horizontal, explode, read-csv, silent-changes]
level: practitioner
status: docs-checked
description: "Upgrade to Polars 2.0: lazy collect defaults to streaming (row order), read_csv/read_ipc changes, concat horizontal, explode, supertypes, SQL decimal and file-seek changes."
sources:
  - https://docs.pola.rs/releases/upgrade/2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Polars 2.0: engine switch and silent behaviour changes

## Streaming is the lazy default
`LazyFrame.collect`/`collect_async` keep `engine="auto"`, which now resolves to streaming for lazy queries (eager `DataFrame` ops still use in-memory; `sink_*` already streamed). Row order is not guaranteed for `unpivot`, `group_by`, joins. Fix by sorting, or `join(..., how="left", maintain_order="left")`. Restore the old engine: `pl.Config.set_engine_affinity("in-memory")`, `lf.collect(engine="in-memory")`, or env `POLARS_ENGINE_AFFINITY=in-memory`. `pl.sql(..., eager=True)` and `SQLContext.execute(eager=True)` now go through `collect()`; for in-memory use `eager=False` then `.collect(engine="in-memory")`. `show_graph()` defaults to `plan_stage="physical"` (use `"ir"` for the old output). `LazyFrame.profile()` is removed (the page says Polars Cloud / On-Prem users can use the Query Profiler; see query-monitoring-polars-cloud for the current Polars Nanook naming).

## Readers
- `pl.read_csv` dispatches to `scan_csv(...).collect()`: gains `with_column_names`, `infer_schema_files`, `credential_provider`, `include_file_paths`, `extra_columns`, `missing_columns`; loses `n_threads`, `batch_size`, `sample_size`, `rechunk`. A `schema_overrides` list must cover every column; `columns=[2,1,3]` keeps requested order.
- `read_ipc` loses `memory_map` and `rechunk`; `scan_ipc` loses `memory_map`.
- CSV `infer_schema_files` defaults to 10 files; headerless names start at `column_0`; a given `schema` is matched by name and file order is respected (use `extra_columns="ignore"`, `missing_columns="insert"`).
- Reading from `io.BytesIO` no longer rewinds: call `buf.seek(0)` after writing.
- Parquet `ENUM` reads as `String`; Arrow/Parquet/Iceberg maps load as `pl.Map` (`dict` values; use `pl.col("m").map.entries()` for the old list-of-structs); unknown Arrow extension types load as `pl.Extension` (`.ext.storage()` or `POLARS_UNKNOWN_EXTENSION_TYPE_BEHAVIOR=load_as_storage`).

## Silent result changes (flagged danger)
- `pl.concat(how="horizontal")` requires equal heights; use `how="horizontal_extend"` to pad with null. `strict=False` raises.
- `explode()` has `empty_as_null=False`: empty lists give zero rows (`empty_as_null=True` for old).
- Signed int + `UInt64` supertype is `Int128` (was Float64).
- `selector & pl.col(...)` is now element-wise bitwise; use `pl.selectors.by_name`.
- `pl.datetime` and `pl.repeat` name outputs after their leftmost argument (or `"literal"`).
- List/array `to_struct` keeps outer nulls; Decimal `round/ceil/floor/sign` widen to `Decimal(p+1, s)`.
- `from_arrow` of a stream-only object returns a `Series` (struct for multi-column).
- Zero-width frames keep height (`df.drop("*").shape` is `(3, 0)`); `pl.DataFrame(height=2)` builds from scratch.
- `is_in()` is strict: lossy coercion raises, Decimal needles in float data raise, naive vs tz-aware raises.
- `shift(None)` raises. The interchange protocol (`__dataframe__`) is removed; use `to_arrow`/`to_pandas`.

## SQL
Query resolution is deferred to `collect()` (use `.collect_schema()` to validate early). Decimal `*` returns summed scales, `/` follows `max(s1, min(s1+6, 12))`; exact literals like `1.5` are `Decimal`; `%`, `DIV` truncate toward zero.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/releases/upgrade/2/. Corrected: Reworded the profile() removal to the page's Query Profiler wording and pointed to the Nanook skill. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.

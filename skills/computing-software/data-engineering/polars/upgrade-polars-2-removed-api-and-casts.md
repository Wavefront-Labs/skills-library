---
id: computing-software.data-engineering.polars.upgrade-polars-2-removed-api-and-casts
name: upgrade-polars-2-removed-api-and-casts
category: computing-software
field: data-engineering
product: polars
tags: [polars-upgrade-2, removed-api, deprecations, casts, argument-removed-error, attribute-removed-error, bin-intervals, to-struct]
level: practitioner
status: docs-checked
description: "Fix Polars 2.0 errors from removed APIs and casts: melt, with_row_count, join_nulls, string-to-date cast, list.to_struct, cut/qcut deprecation, typed removal errors."
sources:
  - https://docs.pola.rs/releases/upgrade/2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Polars 2.0: removed API, casts, reshapes

Most removed items raise new typed errors with a hint: `polars.exceptions.AttributeRemovedError` (an `AttributeError`) for methods/attributes and `ArgumentRemovedError` (a `TypeError`) for parameters. Some still raise plain `AttributeError`/`TypeError`/`ImportError` (e.g. `str.explode()`, `missing_utf8_is_empty_string`, `polars.type_aliases`, `how="outer"` which raises `ValueError`). `POLARS_AUTO_STRUCTIFY` and `POLARS_STREAMING_CHUNK_SIZE` env vars are silently ignored.

## Renames (old to new)
- `melt()` to `unpivot()` (`index`, `on`); `with_row_count()` to `with_row_index()` (default column `"index"`, not `"row_nr"`)
- `join(join_nulls=)` to `nulls_equal=`; `pivot(columns=)` to `on=`; `pl.Array(width=)` to `shape=`
- `group_by(...).count()` to `len()`; `LazyFrame.fetch()` to `collect()` with `head()`
- `streaming=True` to `engine="streaming"`; `explain(tree_format=)` to `format="tree"`
- `top_k/bottom_k(descending=)` to `reverse=`; `rolling_*(min_periods=)` to `min_samples=`
- `read_csv(dtypes=)` to `schema_overrides=`; `row_count_name` to `row_index_name`
- `read_csv_batched()` to `scan_csv().collect_batches()`; `missing_utf8_is_empty_string` to `empty_string_is_null` (boolean inverted)
- `allow_missing_columns=` to `missing_columns="insert"`/`"raise"`
- `str.concat()` to `str.join()` (default delimiter now `""`, not `"-"`)
- `read/scan_*(rechunk=)`: call `.rechunk()` on the result
- Individual optimization flags (`predicate_pushdown`, `no_optimization`, ...) to `optimizations=pl.QueryOptFlags(...)`
- `sink_*(retries=)` to `max_retries` in `storage_options`; `write_ipc(future=)` to `compat_level=`

## Casts and operations that now raise
- int to categorical/Enum and back (page example is `pl.Enum`): use `.cat.to(dtype)` / `.cat.physical()`
- `String` to `Date`/`Datetime`/`Time` cast: use `str.to_date()`, `str.to_datetime()`, `str.to_time()` (SQL `CAST` still works)
- non-nested to `pl.List(..)`: use `pl.list(expr)`
- Boolean `&` integer: cast the boolean first
- `std()/var()` on `Duration`: e.g. `.dt.total_microseconds().std()`
- struct casts with different fields under `strict=True`: use `strict=False` to keep truncation
- flat arguments to `list.gather`, `str.contains_any`, `str.replace_many`: wrap with `implode`
- `log/log1p/exp` on non-numeric input

## API reshapes
- `list.to_struct(fields)`: `fields` is now required and positional; `n_field_strategy`, `upper_bound` removed (e.g. `fields=[f"field_{i}" for i in range(3)]`). `arr.to_struct()` may still omit `fields`.
- `add_business_days` (args after `n`) and `str.to_decimal(inference_length=)` are keyword-only.
- `hash()` takes a single seed (hash values changed; not stable across versions).
- `Series.search_sorted` rejects a Python list: use `pl.Series([...])` or `pl.lit([...])`.
- `struct.rename_fields` needs the exact number of names (`struct.drop` first).
- `pl.Categorical(ordering=)` removed; ordering is lexical.

## Deprecations
`read_avro`/`write_avro` unstable (`pl.Config.warn_unstable(True)`). `cut()`/`qcut()` deprecated for `bin_intervals`, `bin_quantiles`, `bin_ranks`: bins are left-closed (pass `right_closed=True` to match), `labels` is required, `include_breaks` becomes `include_intervals`.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/releases/upgrade/2/. Corrected: Clarified that the int-to-categorical cast example uses pl.Enum. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.

---
id: computing-software.data-engineering.polars.upgrade-polars-0-to-1-breaking-changes
name: upgrade-polars-0-to-1-breaking-changes
category: computing-software
field: data-engineering
product: polars
tags: [polars-upgrade-1, upgrade, breaking-changes, version-1-0, series-constructor, hive-partitioning, replace-strict, collect-schema]
level: practitioner
status: docs-checked
description: "Migrate code to Polars 1.0: strict Series constructor, orient=row, time zone conversion, parquet hive default, replace_strict, pivot, serialize, pl.sql, collect_schema."
sources:
  - https://docs.pola.rs/releases/upgrade/1/
  - https://docs.pola.rs/releases/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrade to Polars 1.0

Upgrade guides list breaking changes that were not previously deprecated plus significant new deprecations. Tip: first upgrade to the latest non-breaking version and fix deprecation warnings; the polars-upgrade tool (pyupgrade-style) can auto-upgrade code. No Rust upgrade guides exist yet.

## Silent / high-risk
- **Time zones in the Series constructor:** values are now always converted to the dtype's zone. `pl.Series([datetime(2020,1,1)], dtype=pl.Datetime('us','Europe/Amsterdam'))` went from `00:00 CET` to `01:00 CET`. Check any pipeline using time zones.
- **`group_by_dynamic` default `offset`** changed from negative `every` to zero; the first window no longer starts before the data (e.g. no `2019-12-31` window).
- **`Series.equals`** no longer compares names; use `check_names=True`.
- **`clip`** keeps the original value where the bound is null.
- **`ewm_mean/std/var`** preserve nulls; call `.forward_fill()` for old behaviour.

## Constructors and types
- `pl.Series([1, 2, 3.5])` now raises `TypeError`; pass `strict=False` (gives f64; with `dtype=pl.Int8` gives 1, 2, 3).
- `pl.DataFrame(data)` no longer infers orientation from dtypes; pass `orient="row"` for row data.
- `reshape` and 2D NumPy arrays now give `Array`; use `.arr.to_list()` for lists.
- Arrow Decimals load as Polars Decimal; `Config.activate_decimals` removed.
- Some DataTypes lost class variables (`pl.Datetime.time_unit`); use `getattr(dtype, "time_unit", None)`.

## API changes
- `replace` keeps the dtype; use `replace_strict` (raises on unmapped values unless `default`).
- `pivot(on, index=..., values=...)`: `columns` renamed `on`, first positional; multi-value names like `test_1_maths`.
- `read/scan_parquet`: Hive partitioning off by default for file inputs (files, globs, lists); on for directories. Pass `hive_partitioning=True`.
- `str.to_datetime` with `%f`/`%.f` defaults to microseconds.
- `get`/`gather` raise on out-of-bounds; `null_on_oob=True` restores nulls.
- `set_sorted` takes one column; call repeatedly.
- `pl.nth(1, "a")` removed `columns`; use `pl.col("a").get(1)`.
- `rle` struct fields are `len` (UInt32) and `value`.
- `read_excel` default engine is `calamine` (no `engine_options`; use `engine="xlsx2csv"`). Extras renamed: use `polars[calamine,async,graph]`.
- `write_json` is row-oriented only; `read_json` can't read `serialize` output, use `DataFrame.deserialize`. `serialize` defaults to binary (use `BytesIO`; `format="json"` for JSON).
- `DataFrame.sql`/`LazyFrame.sql` can't see globals; use `pl.sql(..., eager=True)`.
- Error types shifted: `ComputeError` to `InvalidOperationError`/`SchemaError`.
- Type alias re-exports (`pl.PolarsDataType`) removed.

## Deprecation
LazyFrame `schema`/`dtypes`/`columns`/`width` raise `PerformanceWarning`: use `LazyFrame.collect_schema()`.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/releases/upgrade/1/; https://docs.pola.rs/releases/upgrade/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.

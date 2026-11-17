---
id: computing-software.data-engineering.polars.polars-rust-feature-flags
name: polars-rust-feature-flags
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-installation, rust, cargo, feature-flags, lazy, bigidx, streaming]
level: practitioner
status: docs-checked
description: "Add Polars to a Rust project with cargo and enable opt-in feature flags for lazy, dtypes, IO, streaming, bigidx, and expression operations."
sources:
  - https://docs.pola.rs/user-guide/installation/
  - https://docs.pola.rs/user-guide/expressions/expression-expansion/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Add Polars to Rust and enable feature flags

Goal: a Rust crate that depends on `polars` with exactly the features it needs.

## Install and import

```shell
cargo add polars -F lazy
```

Or in Cargo.toml:

```toml
[dependencies]
polars = { version = "x", features = ["lazy", ...] }
```

```rust
use polars::prelude::*;
```

Big index (more than 2^32 rows): `cargo add polars -F bigidx`. It switches to a `u64` index; Polars is a bit slower with it because many data structures are less cache efficient.

## Feature flags the page lists

- Data types: `dtype-date`, `dtype-datetime`, `dtype-time`, `dtype-duration`, `dtype-i8`, `dtype-i16`, `dtype-i128`, `dtype-u8`, `dtype-u16`, `dtype-u128`, `dtype-categorical`, `dtype-struct`.
- `lazy` (Lazy API), with `regex` (regexes in column selection) and `dot_diagram`.
- `sql` (pass SQL queries), `streaming` (datasets larger than RAM), `random`, `ndarray`, `temporal` (Chrono conversions), `timezones`, `object`, `fmt` (dataframe formatting).
- Strings: `strings`, `string_pad`, `string_to_integer`.
- Performance: `nightly`, `performant` (more fast paths, slower compile), `bigidx`, `cse` (common subplan elimination).
- IO: `serde`, `serde-lazy`, `parquet`, `json`, `ipc`, `decompress` (gzip, zlib, zstd for csv).
- Dataframe operations: `dynamic_group_by` (also enables rolling group by), `sort_multiple`, `rows` (also enables pivot and transpose), `join_asof`, `cross_join`, `semi_anti_join`, `row_hash`, `diagonal_concat`, `dataframe_arithmetic`, `partition_by`.
- Series/expression ops include `is_in`, `concat_str` (linear-time string concatenation), `rolling_window`, `cum_agg`, `rank`, `mode`, `list_eval`, `arg_where`, `search_sorted`, `propagate_nans`, `unique_counts`, `product`, `diff`, `pct_change`.

## Gotchas

- The optional dependencies are optional to minimise the footprint; the page says each user-guide section mentions when it needs an additional dependency.
- The page's sample Cargo.toml pins an old `version = "0.26.1"` with `lazy`, `temporal`, `describe`, `json`, `parquet`, `dtype-datetime`; treat the version as an example, not a recommendation.
- The expression-expansion page says selectors are not available in Rust yet and points to Polars issue #10594.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/installation/; https://docs.pola.rs/user-guide/expressions/expression-expansion/. Corrected: Reworded the fmt and optional-features wording to the page; replaced the unsupported glimpse/selectors claim with the expression-expansion page's statement that selectors are not available in Rust yet; replaced the getting-started source with the expression-expansion page. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.

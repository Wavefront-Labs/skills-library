---
id: computing-software.data-engineering.polars.io-plugin-custom-source
name: io-plugin-custom-source
category: computing-software
field: data-engineering
product: polars
tags: [polars-io-plugins, io-plugin, register-io-source, scan, lazyframe, predicate-pushdown, projection-pushdown, custom-reader]
level: advanced
status: docs-checked
description: "Register a custom file format as a lazy Polars source with register_io_source, honouring with_columns, predicate, n_rows and batch_size pushdowns."
sources:
  - https://docs.pola.rs/user-guide/plugins/io_plugins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IO plugins

Use when a source format is unsupported by Polars and you want projection pushdown, predicate pushdown, early stopping and streaming-engine support. IO plugins are interfaced via Python for now; Rust readers can move data zero-copy over Arrow FFI, needing the GIL only briefly.

```python
import polars as pl
from polars.io.plugins import register_io_source
from typing import Iterator
```

## 1. Provide the schema
Every `scan` must supply the full schema (independent of projection):
```python
def parse_schema(csv_str: str) -> pl.Schema:
    first_line = csv_str.split("\n")[0]
    return pl.Schema({k: pl.String for k in first_line.split(",")})
```
`parse_schema("a,b,c\n1,2,3")` prints `Schema([('a', String), ('b', String), ('c', String)])`.

## 2. Outer function and generator
The outer user-facing function takes the file and options, then returns `register_io_source(io_source=source_generator, schema=schema)`. The callable returns a generator of `pl.DataFrame`. Its arguments are predefined:
- `with_columns: list[str] | None` - columns projected; the reader must project them.
- `predicate: pl.Expr | None` - the reader must filter rows accordingly.
- `n_rows: int | None` - materialize only n rows; the reader can stop early.
- `batch_size: int | None` - hint for the batch size the generator should produce.

```python
def source_generator(with_columns, predicate, n_rows, batch_size) -> Iterator[pl.DataFrame]:
    ...
    df = pl.from_records(rows, schema=schema, orient="row")
    if with_columns is not None:
        df = df.select(with_columns)
    if predicate is not None:
        df = df.filter(predicate)
    yield df
```
The guide's toy reader applies projection and predicate after reading; a performant reader would not read excluded columns at all, and could parse the predicate to skip rows/groups. It decrements `n_rows` by `df.height` per batch and never reads more than requested.

## 3. Use it
`my_scan_csv(csv_str1).collect()` returns all rows as String columns; `my_scan_csv(csv_str2).head(2).collect()` returns only 2 rows.

## For engine authors
Polars calls a wrapper that deserializes the predicate. To identify a registered source, check `isinstance(scan_fn, IOSourceScanFunction)` (from `polars.io.plugins`) and read `scan_fn.io_source`, exactly the object passed to `register_io_source`. As unstable as the rest of the IO plugin API.

The page links a Rust example.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). Removed or trimmed claims the cited page does not confirm.

Method: documentation only; no commands were run.

---
id: computing-software.data-engineering.polars.io-excel-read-write
name: io-excel-read-write
category: computing-software
field: data-engineering
product: polars
tags: [polars, io, excel, read-excel, write-excel, fastexcel, xlsxwriter, polars-io-excel, openpyxl]
level: practitioner
status: docs-checked
description: "Read .xlsx with pl.read_excel (fastexcel, xlsx2csv or openpyxl engines, sheet_name) and write with write_excel (xlsxwriter, worksheet) in Polars."
sources:
  - https://docs.pola.rs/user-guide/io/excel/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read and write Excel files from Python Polars. For performance the page recommends other formats such as Parquet or CSV when possible.

Read
Polars has no native Excel reader; it uses an engine library:
- fastexcel (default, recommended): based on the Rust calamine crate, by far the fastest; reads .xlsx into Arrow memory that Polars uses without copying.
- xlsx2csv: parses the .xlsx to an in-memory CSV which Polars reads with its CSV reader.
- openpyxl: typically slower than xlsx2csv, but more flexible for files that are difficult to parse.

xlsx2csv and openpyxl are slower but may have more features for tricky data; try them if fastexcel fails on a file. Install the engine package(s): `pip install fastexcel xlsx2csv openpyxl`.

```python
df = pl.read_excel("docs/assets/data/path.xlsx")
df = pl.read_excel("docs/assets/data/path.xlsx", sheet_name="Sales")
```
Without `sheet_name`, the first sheet is read.

Write
Install xlsxwriter: `pip install xlsxwriter`.
```python
df = pl.DataFrame({"foo": [1, 2, 3], "bar": [None, "bak", "baz"]})
df.write_excel("docs/assets/data/path.xlsx")
df.write_excel("docs/assets/data/path.xlsx", worksheet="Sales")
```
`worksheet` sets the sheet name. Polars can produce rich Excel files with multiple sheets and formatting; see the API docs for `write_excel`.

Gotcha: writing Excel is not currently available in Rust Polars; the page links a crate for Rust.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). Removed or trimmed claims the cited page does not confirm.

Method: documentation only; no commands were run.

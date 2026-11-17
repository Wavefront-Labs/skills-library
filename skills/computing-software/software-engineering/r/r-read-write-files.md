---
id: computing-software.software-engineering.r.r-read-write-files
name: r-read-write-files
category: computing-software
field: software-engineering
product: r
tags: [r, r-io, read-write-files]
level: practitioner
status: draft
description: "Read and write CSV, RDS and Parquet reliably with explicit types, encodings and NA strings."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# read.csv, readr, data.table::fread and Arrow
- `readr::read_csv(f, col_types = cols(id = col_character()))` avoids guessed types dropping leading zeros; check `problems()`.
- `data.table::fread()` is a fast delimited reader; `arrow::read_parquet()` for columnar data.
- `saveRDS(obj, f)` / `readRDS(f)` keep R classes; `save()`/`load()` restore under the saved names, so prefer RDS.
- `write.csv(df, row.names = FALSE)`; set `fileEncoding = "UTF-8"`.
- Excel: `readxl::read_excel(path, sheet = , na = )`; `writexl::write_xlsx`.
Verify: re-read the written file and compare with `all.equal()`.

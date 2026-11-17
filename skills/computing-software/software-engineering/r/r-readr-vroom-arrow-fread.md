---
id: computing-software.software-engineering.r.r-readr-vroom-arrow-fread
name: r-readr-vroom-arrow-fread
category: computing-software
field: software-engineering
product: r
tags: [r, readr-vroom-arrow-fread]
level: practitioner
status: draft
description: "Import/export large R datasets: readr col_types, fread, arrow Parquet and Feather, and encoding handling."
sources: ["https://cran.r-project.org/doc/manuals/r-release/R-lang.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fast import
- `readr::read_csv(f, col_types = cols(id = col_character()), locale = locale(encoding = "UTF-8"))`; `problems()` shows parse issues.
- `data.table::fread(f, select = c(...), nrows = 1e5)` auto-detects separators.
- `arrow::read_parquet`, `open_dataset(path) |> filter(...) |> collect()` for larger-than-memory; `write_parquet`.
- Base `saveRDS`/`readRDS` preserve types; `write.csv(row.names = FALSE)`.
Verify: round-trip a data frame and `identical()` compare.

---
id: computing-software.software-engineering.r.r-data-table-syntax
name: r-data-table-syntax
category: computing-software
field: software-engineering
product: r
tags: [r, r-data-table, data-table-syntax]
level: advanced
status: draft
description: "Use DT[i, j, by], update by reference with :=, set keys and avoid copy surprises."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# i, j, by syntax, := and keys
- `DT[x > 1, .(m = mean(y)), by = g]`; `.N` is the group row count, `.SD` with `.SDcols` is the subset of data.
- `DT[, z := a + b]` updates by reference without copying; use `copy(DT)` before modifying if you need the original.
- `setkey(DT, id)` sorts by reference; `DT[other, on = "id"]` joins; `merge()` also works.
- `fread`/`fwrite` for IO; `setDT(df)` converts a data frame in place.
Verify: `tracemem` or `address(DT)` shows whether a copy occurred.

---
id: computing-software.software-engineering.r.r-modify-nested-rapply
name: r-modify-nested-rapply
category: computing-software
field: software-engineering
product: r
tags: [r, modify-nested-rapply]
level: advanced
status: draft
description: "Work with nested R lists: modifyList, rapply, unlist naming, lapply recursion and purrr::pluck."
sources: ["https://cran.r-project.org/doc/manuals/r-release/R-lang.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nested lists
- `modifyList(base, updates)` merges recursively; set an element to NULL to delete it.
- `unlist(x)` flattens with generated names (`a.b1`); `use.names = FALSE` for speed.
- `rapply(x, f, how = "replace")`, `purrr::pluck(x, "a", 2, .default = NA)`, `lengths(x)`.
- JSON via jsonlite maps arrays of objects to data frames unless `simplifyVector = FALSE`.
Verify: round-trip through `modifyList(x, list())` returns x.

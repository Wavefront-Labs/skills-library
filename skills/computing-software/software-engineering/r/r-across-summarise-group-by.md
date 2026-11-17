---
id: computing-software.software-engineering.r.r-across-summarise-group-by
name: r-across-summarise-group-by
category: computing-software
field: software-engineering
product: r
tags: [r, across-summarise-group-by]
level: practitioner
status: draft
description: "Summarise grouped data in dplyr 1.1: across(), pick(), reframe(), .by, and ungroup behaviour."
sources: ["https://cran.r-project.org/doc/manuals/r-release/R-lang.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# dplyr grouping
- `df |> summarise(across(where(is.numeric), list(mean = mean, sd = sd), .names = "{.col}_{.fn}"), .by = grp)`.
- `mutate(rank = row_number(), .by = grp)`; `reframe()` for multi-row results; `slice_max(x, n = 3, by = grp)`.
- `group_by()` persists until `ungroup()`; summarise drops the last grouping level (message).
- `count()`, `add_count()`, `distinct(.keep_all = TRUE)`, `rowwise()` + `c_across`.
Verify: row count of summarise equals number of groups.

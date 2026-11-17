---
id: computing-software.software-engineering.r.r-dplyr-grouped-summaries
name: r-dplyr-grouped-summaries
category: computing-software
field: software-engineering
product: r
tags: [r, r-dplyr, dplyr-grouped-summaries]
level: practitioner
status: draft
description: "Compute grouped summaries and window calculations with group_by, summarise, mutate, across and .by."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# group_by, summarise, mutate and across
- `df |> group_by(g) |> summarise(n = n(), m = mean(x, na.rm = TRUE))`; summarise peels one grouping level, add `.groups = "drop"`.
- dplyr 1.1.0 added per-operation `.by = g` which needs no ungroup.
- `across(where(is.numeric), \(v) mean(v, na.rm = TRUE))` applies to many columns.
- Window functions `lag`, `lead`, `cumsum`, `row_number`, `min_rank` run per group inside `mutate`.
- `ungroup()` after a grouped mutate before further work.
Verify: `group_vars(df)` shows lingering groups.

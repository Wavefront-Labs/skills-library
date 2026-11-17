---
id: computing-software.software-engineering.r.r-tibble-vs-data-frame
name: r-tibble-vs-data-frame
category: computing-software
field: software-engineering
product: r
tags: [r, r-data-frames, tibble-vs-data-frame]
level: practitioner
status: draft
description: "Know the behavioural differences when moving code between data.frame and tibble."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tibbles versus base data frames
- Tibbles never partially match names, never drop to a vector with `[`, and never convert strings to factors.
- Printing shows only the first 10 rows and what fits the screen; use `print(n = Inf)` or `View()`.
- Row names are not kept by tibbles; use `tibble::rownames_to_column()`.
- Tibble columns can be list columns, created via `tibble(a = 1:2, b = list(1, 2:3))`.
Verify: `inherits(x, "tbl_df")` and `str(x)`.

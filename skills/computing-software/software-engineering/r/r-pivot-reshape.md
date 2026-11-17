---
id: computing-software.software-engineering.r.r-pivot-reshape
name: r-pivot-reshape
category: computing-software
field: software-engineering
product: r
tags: [r, r-tidyr, pivot-reshape]
level: practitioner
status: draft
description: "Reshape between wide and long layout with names_to, values_to, names_pattern and values_fn."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# pivot_longer and pivot_wider
- `pivot_longer(df, cols = starts_with("y"), names_to = "year", values_to = "n", names_prefix = "y")`.
- `pivot_wider(df, names_from = k, values_from = v, values_fill = 0)`; duplicates produce list-columns with a warning, fix with `values_fn = sum` or de-duplicate.
- Also `separate_wider_delim()`, `unnest_longer()`, `unnest_wider()`, `drop_na()`, `complete()`, `fill()`.
Verify: row count after longer equals ids times pivoted columns.

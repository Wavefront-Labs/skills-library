---
id: computing-software.software-engineering.r.r-dplyr-joins
name: r-dplyr-joins
category: computing-software
field: software-engineering
product: r
tags: [r, r-dplyr, dplyr-joins]
level: practitioner
status: draft
description: "Use left/inner/full/anti/semi joins with join_by and verify cardinality."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Join types, keys and filtering joins
- `left_join(x, y, by = join_by(id == user_id))`; inequality joins are supported via `join_by`.
- `anti_join` finds unmatched rows, `semi_join` filters without adding columns.
- `relationship = "one-to-one"` or `"many-to-one"` and `unmatched = "error"` raise on surprises (dplyr 1.1.0 or newer).
- NA keys match each other by default; set `na_matches = "never"` when that is wrong.
Verify: `count(y, id) |> filter(n > 1)` before joining.

---
id: computing-software.software-engineering.r.r-merge-joins-bind
name: r-merge-joins-bind
category: computing-software
field: software-engineering
product: r
tags: [r, merge-joins-bind]
level: practitioner
status: draft
description: "Combine R data frames with merge(), dplyr joins, rbind/cbind and bind_rows, with key mismatch checks."
sources: ["https://cran.r-project.org/doc/manuals/r-release/R-lang.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Joining
- Base: `merge(a, b, by = "id", all.x = TRUE)`; dplyr: `left_join(a, b, by = join_by(id))`, `inner_join`, `anti_join`, `semi_join`.
- Duplicate keys multiply rows; check with `count(b, id) |> filter(n > 1)`; dplyr 1.1 supports `relationship =` to assert.
- `rbind` needs matching names; `dplyr::bind_rows(.id = "src")` fills missing columns with NA.
Verify: row count after left_join equals the left table when keys are unique.

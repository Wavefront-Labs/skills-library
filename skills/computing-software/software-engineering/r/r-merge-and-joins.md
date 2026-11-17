---
id: computing-software.software-engineering.r.r-merge-and-joins
name: r-merge-and-joins
category: computing-software
field: software-engineering
product: r
tags: [r, r-data-frames, merge-and-joins]
level: practitioner
status: docs-checked
description: "Use merge() with by, all.x and suffixes and detect many-to-many duplication."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/merge.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Merging data frames in base R
- `merge(x, y, by, by.x, by.y, all = FALSE, all.x = all, all.y = all, sort = TRUE, suffixes = c(".x", ".y"))`: `all.x = TRUE` keeps unmatched rows of `x`; `by.x`/`by.y` name differently named keys.
- `sort = TRUE` sorts the result on the `by` columns; `suffixes` disambiguates shared non-key column names.
Verify: Compare `nrow()` before and after the join.

## Checked

Date: 2026-11-02. Confirmed on: ?merge (all.x, by.x, by.y, sort, suffixes defaults). Removed as not confirmed on those pages: The duplicate-key and anyDuplicated advice and the dplyr relationship= claim (dplyr docs not read here).

Method: documentation only; no commands were run.

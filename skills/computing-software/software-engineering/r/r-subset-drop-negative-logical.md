---
id: computing-software.software-engineering.r.r-subset-drop-negative-logical
name: r-subset-drop-negative-logical
category: computing-software
field: software-engineering
product: r
tags: [r, subset-drop-negative-logical]
level: practitioner
status: docs-checked
description: "Choose R subsetting operators: [ vs [[ vs $, negative and logical indices, drop = FALSE, and partial matching."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/Extract.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/Extract.data.frame.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subsetting
- `m[1, , drop = FALSE]` keeps a matrix; without `drop = FALSE`, indexing a single row or column drops to a vector (`?Extract`).
- Extraction can partially match names: `options(warnPartialMatchDollar = TRUE)` warns when `$` does (`?options`).
- Assigning `NULL` to a data frame column deletes it (`?Extract.data.frame`).
Verify: `str(df["a"])` is a data frame, `str(df[["a"]])` a vector.

## Checked

Date: 2026-11-02. Confirmed on: ?Extract (drop = FALSE example), ?options (warnPartialMatchDollar), ?Extract.data.frame (NULL deletes the column). Removed as not confirmed on those pages: Logical-index recycling, tibble partial-match behaviour, x[10] <- 1 padding, and list element removal (not read on these pages).

Method: documentation only; no commands were run.

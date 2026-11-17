---
id: computing-software.software-engineering.r.r-null-vs-na
name: r-null-vs-na
category: computing-software
field: software-engineering
product: r
tags: [r, r-missing, null-vs-na]
level: practitioner
status: docs-checked
description: "Distinguish NULL from NA, handle zero-length input in loops and functions, and remove list elements with NULL."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/NULL.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/Extract.data.frame.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/seq.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NULL versus NA and zero-length vectors
- `seq_len(n)` and `seq_along(x)` are safe for empty input; `1:length(x)` is not (`?seq`).
- Assigning `NULL` to a data frame column with `$<-` deletes the column (`?Extract.data.frame`).
- `is.null(x)` tests for `NULL` (`?NULL`).
Verify: Call the function with `NULL` and `character(0)` inputs.

## Checked

Date: 2026-11-02. Confirmed on: ?seq, ?Extract.data.frame (NULL deletes the column), ?NULL. Removed as not confirmed on those pages: length(NULL), c(1, NULL), the list-element removal and store-NULL idioms (not read on these pages).

Method: documentation only; no commands were run.

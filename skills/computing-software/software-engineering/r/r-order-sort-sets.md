---
id: computing-software.software-engineering.r.r-order-sort-sets
name: r-order-sort-sets
category: computing-software
field: software-engineering
product: r
tags: [r, r-sorting, order-sort-sets]
level: practitioner
status: docs-checked
description: "Sort by multiple keys and use match, %in%, duplicated and set functions correctly."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/order.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# order, sort, unique, match and set operations
- `order` returns a permutation; ties in the first key are broken by later keys, and the sort is stable (except `method = "quick"`).
- `na.last = TRUE` is the default for `order`, putting missing values last; `decreasing = FALSE` is the default and for `method = "radix"` it can be a vector.
- Character ordering depends on the locale's collating sequence, except for `method = "radix"`.
Verify: compare `Sys.getlocale("LC_COLLATE")` across machines for reproducibility.

## Checked

Date: 2026-11-02. Confirmed on ?order (na.last default, decreasing, tie-breaking and stability, radix versus locale). Removed as not confirmed: sort() defaults, `%in%`/match equivalence, duplicated, set operations, the C-locale wording.

Method: documentation only; no commands were run.

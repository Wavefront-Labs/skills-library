---
id: computing-software.software-engineering.r.r-na-handling
name: r-na-handling
category: computing-software
field: software-engineering
product: r
tags: [r, r-missing, na-handling]
level: practitioner
status: docs-checked
description: "Handle NA, NaN, NULL and Inf correctly in tests, aggregates and joins."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/NA.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NA propagation and na.rm
- NA is a missing TRUE/FALSE value in logical operations and gives a definite result when the NA does not affect the outcome, e.g. `NA & FALSE` is FALSE.
- `is.na()` is TRUE for `NA` and, in numeric and complex vectors, for `NaN`.
- Typed missing constants exist: `NA_integer_`, `NA_real_`, `NA_complex_` and `NA_character_`; the character NA is distinct from the string `"NA"`.
Verify: `anyNA(x)` before modelling.

## Checked

Date: 2026-11-02. Confirmed on ?NA (logical NA semantics, is.na on NaN, typed NA constants). Removed as not confirmed on that page: na.rm advice, max(numeric(0)), complete.cases/na.omit, the `if (NA)` error, is.nan(NA).

Method: documentation only; no commands were run.

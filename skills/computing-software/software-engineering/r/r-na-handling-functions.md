---
id: computing-software.software-engineering.r.r-na-handling-functions
name: r-na-handling-functions
category: computing-software
field: software-engineering
product: r
tags: [r, na-handling-functions]
level: practitioner
status: docs-checked
description: "Handle NA in R: is.na, na.rm arguments, complete.cases, na.omit, and the NA propagation in logic."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/NA.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/is.finite.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NA handling
- `NA_integer_`, `NA_real_`, `NA_complex_` and `NA_character_` are typed NA constants (`?NA`).
- Test with `is.na(x)`; `is.nan` and `is.finite` are documented separately (`?is.finite`).
- `NA` is a logical constant; `NA & FALSE` is FALSE because the result does not depend on the NA (`?NA`).
Verify: `anyNA(x)` before modelling.

## Checked

Date: 2026-11-02. Confirmed on: ?NA, ?is.finite. Removed as not confirmed on those pages: The na.omit/complete.cases/tidyr advice, the mean(na.rm) example, and the NULL remark (not read on these pages).

Method: documentation only; no commands were run.

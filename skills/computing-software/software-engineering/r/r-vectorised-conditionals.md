---
id: computing-software.software-engineering.r.r-vectorised-conditionals
name: r-vectorised-conditionals
category: computing-software
field: software-engineering
product: r
tags: [r, r-control-flow, vectorised-conditionals]
level: practitioner
status: docs-checked
description: "Pick if/else versus ifelse versus switch and avoid ifelse type and attribute loss."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/ifelse.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/Control.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/switch.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ifelse and switch
- In `if`, a condition of length greater than one is an error (`?Control`); use `ifelse()` for vectors.
- `ifelse()` returns a vector with the shape of `test` and strips other attributes such as Date class (`?ifelse`).
- `switch(EXPR, ...)` selects among alternatives (`?switch`).
Verify: Pass NA and a length-2 vector to the condition.

## Checked

Date: 2026-11-02. Confirmed on: ?Control (length-greater-than-one condition is an error), ?ifelse (attribute handling), ?switch. Removed as not confirmed on those pages: The R 4.2.0 version, dplyr::if_else, switch fall-through details, and the && / || remark (not read on these pages).

Method: documentation only; no commands were run.

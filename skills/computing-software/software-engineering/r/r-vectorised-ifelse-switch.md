---
id: computing-software.software-engineering.r.r-vectorised-ifelse-switch
name: r-vectorised-ifelse-switch
category: computing-software
field: software-engineering
product: r
tags: [r, vectorised-ifelse-switch]
level: practitioner
status: docs-checked
description: "Branch vectorised in R with ifelse, dplyr::case_when, switch, and avoid scalar if on vectors."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/ifelse.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/Control.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/switch.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditionals
- `if` needs a condition of length one; longer conditions are an error (`?Control`).
- `ifelse(test, yes, no)` is vectorised but drops attributes (`?ifelse`).
- `switch(EXPR, ...)` selects among alternatives (`?switch`).
Verify: Check `ifelse(c(TRUE, NA), 1, 2)` for yourself.

## Checked

Date: 2026-11-02. Confirmed on: ?Control, ?ifelse, ?switch. Removed as not confirmed on those pages: dplyr if_else/case_when, the R >= 4.2 gate, switch fall-through and the isTRUE/any/all line (not read on these pages).

Method: documentation only; no commands were run.

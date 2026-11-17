---
id: computing-software.software-engineering.r.r-factor-levels-relevel-forcats
name: r-factor-levels-relevel-forcats
category: computing-software
field: software-engineering
product: r
tags: [r, factor-levels-relevel-forcats]
level: practitioner
status: draft
description: "Control R factor level order and recoding with factor(), relevel, droplevels and forcats functions."
sources: ["https://cran.r-project.org/doc/manuals/r-release/R-lang.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Factors
- `factor(x, levels = c("low","mid","high"), ordered = TRUE)`; `levels(f)`, `droplevels(f)`, `relevel(f, ref = "b")`.
- Integer codes: `as.integer(f)`; convert numeric factors with `as.numeric(as.character(f))`.
- forcats: `fct_reorder(f, x)`, `fct_infreq`, `fct_lump_n(f, 5)`, `fct_recode`, `fct_collapse`.
- `stringsAsFactors = FALSE` is default since R 4.0.
Verify: after subsetting, `table(f)` still lists unused levels until `droplevels`.

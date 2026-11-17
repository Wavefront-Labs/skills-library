---
id: computing-software.software-engineering.r.r-factor-levels
name: r-factor-levels
category: computing-software
field: software-engineering
product: r
tags: [r, r-factors, factor-levels]
level: practitioner
status: draft
description: "Control level order, drop unused levels, convert factors safely and use forcats helpers."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Factor levels, ordering and dropping
- Since R 4.0.0 `stringsAsFactors` defaults to FALSE; set levels explicitly with `factor(x, levels = c("lo","hi"))`.
- Values not in `levels` become NA; check with `table(x, useNA = "ifany")`.
- Subsetting keeps unused levels; call `droplevels()`, otherwise `table()` and plots show empty categories.
- Never `as.numeric(f)` on a factor of numbers (gives codes); use `as.numeric(as.character(f))`.
- forcats: `fct_relevel`, `fct_reorder`, `fct_lump_n`, `fct_infreq`.
Verify: `levels(f)` and `nlevels(f)` after every transform.

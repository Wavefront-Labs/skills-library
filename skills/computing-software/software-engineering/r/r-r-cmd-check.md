---
id: computing-software.software-engineering.r.r-r-cmd-check
name: r-r-cmd-check
category: computing-software
field: software-engineering
product: r
tags: [r, r-packages, r-cmd-check]
level: advanced
status: docs-checked
description: "Run R CMD check --as-cran, fix NOTEs and meet CRAN policies before submitting."
sources: ["https://cran.r-project.org/doc/manuals/r-release/R-exts.html", "https://stat.ethz.ch/R-manual/R-devel/library/utils/html/globalVariables.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# R CMD check and CRAN submission
- `R CMD check --as-cran` enables CRAN-style checks (Writing R Extensions).
- `utils::globalVariables()` declares names to silence undefined-global NOTEs (`?globalVariables`).
Verify: Check passes on the built tarball with `R CMD check --as-cran`.

## Checked

Date: 2026-11-02. Confirmed on: R-exts (--as-cran), ?globalVariables. Removed as not confirmed on those pages: CRAN policy statements (two-core limit, home directory), devtools::check_win_devel, and cran-comments.md (policy pages not read here).

Method: documentation only; no commands were run.

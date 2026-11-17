---
id: computing-software.software-engineering.r.r-subset-operators
name: r-subset-operators
category: computing-software
field: software-engineering
product: r
tags: [r, r-subsetting, subset-operators]
level: practitioner
status: docs-checked
description: "Choose [ , [[ and $ correctly for vectors, lists and data frames, and avoid partial matching surprises."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/Extract.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single bracket, double bracket and dollar
- `m[1, , drop = FALSE]` keeps a one-row matrix (`?Extract`); `[[` has an `exact` argument that controls partial matching (`?Extract`).
- `options(warnPartialMatchDollar = TRUE)` warns if `$` partially matches (`?options`).
Verify: Test with a one-column and one-row input to catch dimension dropping.

## Checked

Date: 2026-11-02. Confirmed on: ?Extract (drop = FALSE, exact), ?options (warnPartialMatchDollar). Removed as not confirmed on those pages: x[NA], tibble drop behaviour and the container-type description (not read on these pages).

Method: documentation only; no commands were run.

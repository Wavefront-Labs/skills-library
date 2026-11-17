---
id: computing-software.software-engineering.r.r-vector-recycling
name: r-vector-recycling
category: computing-software
field: software-engineering
product: r
tags: [r, r-vectors, vector-recycling]
level: practitioner
status: docs-checked
description: "Predict recycling in arithmetic and comparisons, and catch the silent cases that give no warning."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/options.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/stopifnot.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vector recycling and length mismatches
- Guard functions with `stopifnot(length(a) == length(b))` (`?stopifnot`).
- `options(warn = 2)` turns warnings, including recycling warnings, into errors (`?options`).
Verify: Run tests with `options(warn = 2)`.

## Checked

Date: 2026-11-02. Confirmed on: ?stopifnot, ?options (warn level). Removed as not confirmed on those pages: The rules of recycling (multiples, zero-length operand, warning text) and the %in% advice (not read on these pages).

Method: documentation only; no commands were run.

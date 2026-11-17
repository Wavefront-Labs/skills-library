---
id: computing-software.software-engineering.r.r-recycling-coercion-rules
name: r-recycling-coercion-rules
category: computing-software
field: software-engineering
product: r
tags: [r, recycling-coercion-rules]
level: practitioner
status: docs-checked
description: "Predict R vector recycling (with its length warning) and coercion order logical < integer < double < character."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/integer.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/typeof.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/mode.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recycling and coercion
- `as.integer` truncates non-integral numeric values towards zero (`?integer`).
- `typeof`, `mode` and `storage.mode` report different views of an object's type (`?typeof`, `?mode`).
- Use `identical()` for exact comparison and `isTRUE(all.equal(a, b))` for floats.
Verify: `typeof(c(1L, 2.5))` is "double".

## Checked

Date: 2026-11-02. Confirmed on: ?integer (truncation), ?typeof, ?mode, ?all.equal (isTRUE advice). Removed as not confirmed on those pages: The recycling-warning text, the coercion hierarchy list, and the 1:3 == c(1,2,3) example (not read on these pages).

Method: documentation only; no commands were run.

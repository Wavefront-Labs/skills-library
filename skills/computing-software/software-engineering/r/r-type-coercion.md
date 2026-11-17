---
id: computing-software.software-engineering.r.r-type-coercion
name: r-type-coercion
category: computing-software
field: software-engineering
product: r
tags: [r, r-vectors, type-coercion]
level: practitioner
status: docs-checked
description: "Know the logical, integer, double, character coercion order and how c() and ifelse silently coerce."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/integer.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/typeof.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/mode.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implicit coercion and type hierarchy
- `as.integer` truncates non-integral numeric values towards zero (`?integer`).
- `typeof()`, `mode()` and `storage.mode()` report different views of type (`?typeof`, `?mode`); `class()` is separate (`?class`).
- `identical()` is exact; `all.equal()` has a tolerance.
Verify: `typeof()` on the result of every mixed `c()` you rely on.

## Checked

Date: 2026-11-02. Confirmed on: ?integer (truncation), ?typeof, ?mode, ?all.equal. Removed as not confirmed on those pages: The logical < integer < double < character < list hierarchy, the as.integer("3.7") example, and class(matrix(1)) (not read on these pages).

Method: documentation only; no commands were run.

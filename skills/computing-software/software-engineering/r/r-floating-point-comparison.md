---
id: computing-software.software-engineering.r.r-floating-point-comparison
name: r-floating-point-comparison
category: computing-software
field: software-engineering
product: r
tags: [r, r-vectors, floating-point-comparison]
level: practitioner
status: docs-checked
description: "Compare doubles with all.equal or a tolerance, never ==, and use isTRUE around all.equal in conditions."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/all.equal.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Floating-point equality
- `all.equal()` compares with a tolerance (default `sqrt(.Machine$double.eps)`, about 1.5e-8).
- `all.equal()` does not return FALSE on a mismatch, so in `if` expressions use `isTRUE(all.equal(....))` (the page says exactly this).
- `identical()` tests exact equality.
Verify: `isTRUE(all.equal(x, y, tolerance = 1e-10))` in unit tests of numeric code.

## Checked

Date: 2026-11-02. Confirmed on: ?all.equal (tolerance default, 1.5e-8, isTRUE(all.equal(...)) advice). Removed as not confirmed on those pages: Integer overflow and bit64 advice, and the description of what identical() compares (not on this page).

Method: documentation only; no commands were run.

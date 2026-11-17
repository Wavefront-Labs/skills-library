---
id: computing-software.software-engineering.r.r-apply-family
name: r-apply-family
category: computing-software
field: software-engineering
product: r
tags: [r, r-functional, apply-family]
level: practitioner
status: docs-checked
description: "Choose lapply/vapply/Map and avoid sapply's unpredictable return type."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/lapply.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lapply, sapply, vapply and Map
- `sapply` simplifies to a vector, matrix or array only when every result has the same positive length, otherwise it returns a list; simplification is attempted only for non-empty input.
- `vapply(x, f, numeric(1))` always simplifies and checks that each result has the same length and type as `FUN.VALUE`, so prefer it in code.
Verify: `vapply` raises an error if a result has the wrong type.

## Checked

Date: 2026-11-02. Confirmed on ?lapply (sapply simplification rules, vapply FUN.VALUE checking). Removed as not confirmed on that page: Map, mapply SIMPLIFY, Reduce accumulate, apply transposition, do.call(rbind) and faster binders.

Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.r.r-r6-reference-classes
name: r-r6-reference-classes
category: computing-software
field: software-engineering
product: r
tags: [r, r6-reference-classes]
level: advanced
status: draft
description: "Build mutable R6 objects with public/private members, active bindings, inherit and clone(deep = TRUE)."
sources: ["https://cran.r-project.org/doc/manuals/r-release/R-lang.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# R6
- `Acc <- R6Class("Acc", public = list(total = 0, add = function(x) { self$total <- self$total + x; invisible(self) }), private = list(), active = list())`.
- Chain calls via `invisible(self)`; `Child <- R6Class(inherit = Acc)`, `super$add(x)`.
- Reference semantics: `b <- a` shares state; use `a$clone(deep = TRUE)` for nested R6 fields.
- Fields that are R6 objects must be created in `initialize`, not as defaults.
Verify: modify via alias and see the original change.

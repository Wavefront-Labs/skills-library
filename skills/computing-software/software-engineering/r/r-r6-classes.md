---
id: computing-software.software-engineering.r.r-r6-classes
name: r-r6-classes
category: computing-software
field: software-engineering
product: r
tags: [r, r-oop-s4, r6-classes]
level: advanced
status: draft
description: "Build R6 classes with public, private, active fields and understand mutable reference behaviour."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# R6 classes and reference semantics
- `Counter <- R6::R6Class("Counter", public = list(n = 0, add = function() { self$n <- self$n + 1; invisible(self) }))`.
- Objects are environments: `b <- a` does not copy; use `a$clone(deep = TRUE)`.
- Create fields that are R6 objects in `initialize`, not as defaults (defaults are shared across instances).
- Return `invisible(self)` to support method chaining; private fields only through `private$`.
Verify: modify a clone and confirm the original is unchanged.

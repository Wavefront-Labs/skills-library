---
id: computing-software.software-engineering.r.r-lexical-scoping
name: r-lexical-scoping
category: computing-software
field: software-engineering
product: r
tags: [r, r-environments, lexical-scoping]
level: advanced
status: docs-checked
description: "Use closures and <<- correctly and avoid accidental global mutation."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/environment.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/Syntax.html", "https://cran.r-project.org/doc/manuals/r-release/R-lang.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lexical scope, closures and superassignment
- Per R-lang, a function's environment includes a pointer to its enclosing environment, and variable lookup is repeated up the chain.
- `<<-` is the superassignment operator; R-lang explains that it assigns in the enclosing environment.
- `environment(fn)` returns the environment of a function (`?environment`).
Verify: `environment(fn)` and `ls(environment(fn))` show what a closure captured.

## Checked

Date: 2026-11-02. Confirmed on: R-lang (enclosure, superassignment), ?Syntax, ?environment. Removed as not confirmed on those pages: The lookup order wording about attached packages, local(), and the list comparison (not read on these pages).

Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.r.r-lexical-scope-assign-sys-function
name: r-lexical-scope-assign-sys-function
category: computing-software
field: software-engineering
product: r
tags: [r, lexical-scope-assign-sys-function]
level: advanced
status: docs-checked
description: "Understand R lexical scope, superassignment, local(), new.env, get/assign, and parent.frame."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/assign.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/environment.html", "https://cran.r-project.org/doc/manuals/r-release/R-lang.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environments
- R-lang: a function's environment holds an enclosure, a pointer to the enclosing environment, and lookup repeats up the chain.
- `<<-` is the superassignment operator (R-lang, assignment section; `?Syntax` lists it).
- `new.env()`, `assign()`, `environment(fn)`, `parent.frame()`, `sys.call()` and `match.call()` are base functions documented in the `?environment`, `?assign` and related pages.
Verify: A counter closure increments with `<<-`.

## Checked

Date: 2026-11-02. Confirmed on: R-lang (enclosure, superassignment), ?Syntax, ?assign, ?environment. Removed as not confirmed on those pages: Details on exists(inherits=), mget, local(), and the claim that environments are reference objects (not read on these pages).

Method: documentation only; no commands were run.

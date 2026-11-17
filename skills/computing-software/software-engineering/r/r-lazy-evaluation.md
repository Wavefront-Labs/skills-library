---
id: computing-software.software-engineering.r.r-lazy-evaluation
name: r-lazy-evaluation
category: computing-software
field: software-engineering
product: r
tags: [r, r-functions, lazy-evaluation]
level: advanced
status: docs-checked
description: "Understand promises, argument defaults evaluated in the function frame, force() and missing()."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/force.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/missing.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/match.arg.html", "https://cran.r-project.org/doc/manuals/r-release/R-lang.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lazy evaluation, missing and default arguments
- R-lang describes promise objects as the mechanism behind lazy evaluation of arguments.
- `force(x)` forces evaluation of an argument (`?force`).
- `missing(x)` is only reliable if `x` has not been altered (`?missing`); `match.arg` matches an argument against a table of choices (`?match.arg`).
Verify: Call with each argument omitted in turn.

## Checked

Date: 2026-11-02. Confirmed on: R-lang (promise objects), ?force, ?missing, ?match.arg. Removed as not confirmed on those pages: The claims that unused-argument errors never fire, that defaults see local variables, and the loop-closure advice (not read on these pages).

Method: documentation only; no commands were run.

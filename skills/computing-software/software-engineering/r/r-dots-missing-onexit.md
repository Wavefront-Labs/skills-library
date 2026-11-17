---
id: computing-software.software-engineering.r.r-dots-missing-onexit
name: r-dots-missing-onexit
category: computing-software
field: software-engineering
product: r
tags: [r, dots-missing-onexit]
level: advanced
status: docs-checked
description: "Write robust R functions using ..., list(...), missing(), match.arg(), stopifnot() and on.exit(add = TRUE)."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/dots.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/on.exit.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/match.arg.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/missing.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/force.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Function techniques
- `...length()`, `..1` access dots (`?dots`); `missing(x)` tests whether an argument was supplied (`?missing`).
- `match.arg(arg, choices, several.ok = FALSE)` matches an argument against a table of choices (`?match.arg`).
- `on.exit(expr, add = FALSE, after = TRUE)` registers cleanup; `add = TRUE` appends instead of replacing (`?on.exit`).
- `force(x)` forces evaluation of an argument (`?force`).
Verify: An error in the body still triggers the `on.exit` expression.

## Checked

Date: 2026-11-02. Confirmed on: ?dots, ?missing, ?match.arg, ?on.exit, ?force. Removed as not confirmed on those pages: The named stopifnot example with its R >= 4.0 version gate, and the default-argument claims (not on these pages).

Method: documentation only; no commands were run.

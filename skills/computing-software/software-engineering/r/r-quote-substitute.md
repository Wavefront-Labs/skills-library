---
id: computing-software.software-engineering.r.r-quote-substitute
name: r-quote-substitute
category: computing-software
field: software-engineering
product: r
tags: [r, r-meta, quote-substitute]
level: advanced
status: docs-checked
description: "Capture, build and evaluate expressions and know the non-standard-evaluation trap in functions."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/substitute.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/bquote.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/deparse.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/body.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/formals.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/call.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# quote, substitute, bquote and eval
- `substitute`, `bquote`, `deparse`, `body`, `formals` and `as.call` are base functions with the help pages listed in sources.
- `substitute(arg)` inside a function is the usual way to capture the caller's expression; `deparse()` turns it into text.
- `bquote(expr)` quotes with `.()` sub-expressions evaluated (`?bquote`).
Verify: Print the captured call and check it is what you expect.

## Checked

Date: 2026-11-02. Confirmed on: Existence and descriptions of ?substitute, ?bquote, ?deparse, ?body, ?formals, ?call (as.call). Removed as not confirmed on those pages: lobstr::ast, the NSE-twin advice, and eval(expr, envir = list) wording (not read on these pages).

Method: documentation only; no commands were run.

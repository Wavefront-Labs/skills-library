---
id: computing-software.software-engineering.r.r-dots-and-on-exit
name: r-dots-and-on-exit
category: computing-software
field: software-engineering
product: r
tags: [r, r-functions, dots-and-on-exit]
level: practitioner
status: docs-checked
description: "Use ..., list(...), ..1 and on.exit(add = TRUE) for cleanup, and know implicit return."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/dots.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/on.exit.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dots, on.exit and return values
- `...length()` returns the number of expressions in `...`; `..1`, `..2` refer to individual elements (`?dots`).
- `on.exit(expr, add = FALSE, after = TRUE)`: by default a new expression replaces the earlier one; pass `add = TRUE` to keep both (`?on.exit`).
- Pass dots on explicitly: `inner(...)`.
Verify: Raise an error mid-function and confirm the `on.exit` expression ran.

## Checked

Date: 2026-11-02. Confirmed on: ?dots (..1, ...length()), ?on.exit (signature with add and after). Removed as not confirmed on those pages: invisible(), the claim that a misspelled argument name falls into dots silently, and list(...) description.

Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.r.r-style-lintr-styler
name: r-style-lintr-styler
category: computing-software
field: software-engineering
product: r
tags: [r, r-style-linting, style-lintr-styler]
level: practitioner
status: draft
description: "Format code to the tidyverse style with styler and enforce with lintr in CI."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# tidyverse style, styler and lintr
- Style: snake_case names, `<-` for assignment, spaces around operators, 2-space indent, lines up to 80 characters, `TRUE`/`FALSE` not `T`/`F`.
- `styler::style_file("x.R")` or `style_pkg()` rewrites code; `lintr::lint_package()` reports issues; configure in `.lintr`.
- Avoid dots in function names (S3 confusion).
- Run `lintr::lint_package()` in CI to fail on lint.
Verify: lint passes with zero findings.

---
id: computing-software.software-engineering.r.r-purrr-mapping
name: r-purrr-mapping
category: computing-software
field: software-engineering
product: r
tags: [r, r-functional, purrr-mapping]
level: practitioner
status: draft
description: "Use map_*(), map2, pmap, walk and safely/possibly for iteration with error handling."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# purrr map functions
- `map_dbl(x, \(v) v * 2)` (formula shorthand `~ .x * 2` is still accepted); type-suffixed variants error on wrong type.
- `map_dfr` is superseded; use `map(...) |> list_rbind()` (purrr 1.0.0 or newer).
- `possibly(f, otherwise = NA)` and `safely(f)` capture errors per element.
- `walk()` is for side effects and returns its input invisibly.
Verify: `map_chr` on a malformed element should error loudly.

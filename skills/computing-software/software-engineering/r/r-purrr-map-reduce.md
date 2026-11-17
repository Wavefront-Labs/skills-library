---
id: computing-software.software-engineering.r.r-purrr-map-reduce
name: r-purrr-map-reduce
category: computing-software
field: software-engineering
product: r
tags: [r, purrr-map-reduce]
level: practitioner
status: draft
description: "Use purrr 1.x: map_* typed variants, map2/pmap, reduce/accumulate, safely/possibly and walk."
sources: ["https://cran.r-project.org/doc/manuals/r-release/R-lang.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# purrr
- `map_dbl(x, \(v) v * 2)`, `map_chr`, `map_lgl`, `map_df`->`list_rbind(map(...))`; `map2`, `pmap`, `imap`.
- `reduce(xs, `+`)`, `accumulate`; `keep`, `discard`, `detect`; `walk` for side effects.
- Errors: `possibly(f, otherwise = NA)`, `safely(f)` returns result/error pairs.
- Parallel mapping: `in_parallel()` / mirai integration in recent purrr (confirm version).
Verify: `map_dbl(1:3, \(i) i^2)` returns 1 4 9.

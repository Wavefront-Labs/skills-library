---
id: computing-software.software-engineering.r.r-tidy-eval
name: r-tidy-eval
category: computing-software
field: software-engineering
product: r
tags: [r, r-meta, tidy-eval]
level: advanced
status: draft
description: "Write functions around dplyr verbs with {{ }}, .data and := and know when strings need sym()."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data masking and embracing
- `my_mean <- function(df, var) df |> summarise(m = mean({{ var }}))` embraces a bare column.
- Strings: `.data[[col]]` in data-masking verbs; `across(all_of(cols))` in tidy-select verbs.
- Dynamic names: `summarise("{name}_mean" := mean(x))` with glue syntax and `:=`.
- Avoid `eval(parse(text = ...))`; build symbols with `rlang::sym()` and `!!` if necessary.
Verify: call the function with a bare name and with a string via `.data`.

---
id: computing-software.software-engineering.r.r-regex-perl-stringr-glue
name: r-regex-perl-stringr-glue
category: computing-software
field: software-engineering
product: r
tags: [r, regex-perl-stringr-glue]
level: practitioner
status: draft
description: "Use R regex engines (TRE, perl = TRUE, fixed, ICU in stringr), capture groups with regmatches and str_match, glue interpolation."
sources: ["https://cran.r-project.org/doc/manuals/r-release/R-lang.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Regex in R
- Base: `grepl(pat, x, perl = TRUE)`, `sub`/`gsub`, `regmatches(x, regexpr(...))`, `regexec` for groups; escape backslashes twice (`"\\d+"`) or use raw strings `r"(\d+)"` (R >= 4.0).
- stringr (ICU): `str_detect`, `str_extract`, `str_match`, `str_replace_all(x, "(a)(b)", "\\2\\1")`, `str_glue`.
- `fixed = TRUE` for literal matching and speed; `sprintf`, `format`, `formatC`, `trimws`.
Verify: `str_match("a1", "([a-z])(\\d)")` returns two groups.

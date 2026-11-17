---
id: computing-software.software-engineering.r.r-regex-flavours
name: r-regex-flavours
category: computing-software
field: software-engineering
product: r
tags: [r, r-strings, regex-flavours]
level: practitioner
status: docs-checked
description: "Pick TRE, PCRE or fixed matching in base R and escape correctly."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/regex.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/Quotes.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/regmatches.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# grepl, sub, gsub and regex engines
- `perl = TRUE` selects Perl-like regular expressions (`?regex`); lookahead and negative lookahead assertions are described there.
- R raw strings use `r"(...)"` (`?Quotes`), which avoids doubling backslashes.
- `regmatches()` extracts or replaces matched substrings (`?regmatches`).
Verify: Test on strings with dots, brackets and non-ASCII characters.

## Checked

Date: 2026-11-02. Confirmed on: ?regex (perl = TRUE, lookahead), ?Quotes (raw strings), ?regmatches. Removed as not confirmed on those pages: The stringr/ICU line, the R 4.0.0 version, the default-engine name, fixed = TRUE and back-reference wording (not read on these pages).

Method: documentation only; no commands were run.

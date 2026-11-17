---
id: computing-software.software-engineering.c.parsing-numbers-with-strtol
name: parsing-numbers-with-strtol
category: computing-software
field: software-engineering
product: c
tags: [c, strtol, strtod, atoi-pitfalls, errno-erange, parse-integer]
level: practitioner
status: docs-checked
description: "Parse integers and floats with strtol/strtod and full error checking instead of atoi."
sources: ["https://man7.org/linux/man-pages/man3/strtol.3.html", "https://en.cppreference.com/w/c/string/byte/strtol", "https://en.cppreference.com/w/c/string/byte/atoi", "https://en.cppreference.com/w/c/string/byte/strtof"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parsing numbers with strtol

Goal: reject bad numeric input instead of silently returning 0.

- `atoi`/`atof` give no error signal and undefined results on overflow. Use `strtol`, `strtoll`, `strtoul`, `strtod`.
- Pattern: `errno = 0; char *end; long v = strtol(s, &end, 10);` then `end == s` means no digits, `*end != '\0'` means trailing junk, `errno == ERANGE` means out of range.
- Base 0 accepts `0x` hex and leading-0 octal; use 10 for user decimals.
- `strtoul` accepts a leading `-` and negates modulo, so reject `-` yourself for unsigned parsing.
- Narrowing the `long` result to `int` needs a range check against `INT_MIN`/`INT_MAX`.
- `strtod` is locale-dependent for the decimal point; for fixed formats use the "C" locale or parse manually.
- Many projects wrap this in a `parse_long()` helper returning bool.

Verify: unit-test empty string, " 12", "12abc", "99999999999999999999", "-0".

## Checked

- Date: 2026-11-02
- Confirmed: man7 strtol(3) (ERANGE with LONG_MAX/LONG_MIN, errno must be cleared first, base 0/16 accept `0x`, MT-Safe locale); cppreference strtol (optional sign, base 0 prefixes, negation of the result for a leading minus, also for unsigned), atoi (out-of-range result is undefined), strtof (decimal-point character depends on the current C locale). Nothing removed.
Method: documentation only; no commands were run.

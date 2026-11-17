---
id: computing-software.software-engineering.perl.regex-lookaround-anchors
name: regex-lookaround-anchors
category: computing-software
field: software-engineering
product: perl
tags: [perl, lookahead, lookbehind, zero-width, anchors, perlre, regex-lookaround-anchors, perl-regex-advanced]
level: advanced
status: docs-checked
description: "Use (?=), (?!), (?<=), (?<!), b, A, z and G for zero-width assertions, and know the lookbehind width limits."
sources: ["https://perldoc.perl.org/perlre", "https://perldoc.perl.org/perlrecharclass"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lookahead, lookbehind and anchors

**Goal:** assert context without consuming it.

```perl
/foo(?=bar)/      # foo followed by bar (bar not consumed)
/foo(?!bar)/      # foo not followed by bar
/(?<=\$)\d+/      # digits preceded by $
/(?<!\w)cat(?!\w)/  # whole word without relying on \b
s/(?<=\d)(?=(?:\d{3})+\b)/,/g;   # thousands separators: 1234567 -> 1,234,567
/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/   # password rule checks
```

## Rules
- Lookbehind must have a bounded width. Alternatives of different fixed lengths are fine: `(?<=a|bc)`. Variable-length lookbehind (at most 255 characters) arrived experimentally in 5.30 and is mostly no longer experimental in 5.36 (perl5360delta; read the exact limits in perlre).
- `\K` is a workaround for variable-length lookbehind in substitutions.
- `\b` is a boundary between `\w` and `\W`; `\b{wb}` (5.22+) is a Unicode word boundary.
- Anchors: `\A` start of string, `\z` end of string, `\Z` end or before final newline, `^`/`$` per line only under `/m`. Prefer `\A`/`\z` for validation of whole values, because `$` accepts a trailing newline: `"abc\n" =~ /^abc$/` is true.
- Lookahead can be nested and contain captures.
- `\G` asserts the position of the end of the previous `//g` match (see lexers).

## Failure modes
- `(?<=\s*)` dies "Lookbehind longer than 255 not implemented" or "Variable length lookbehind not implemented".
- Validating with `^...$` and no `\z` lets a value with a trailing newline pass.

## Self-check
- [ ] `perl -e '$_="1234567"; s/(?<=\d)(?=(?:\d{3})+\z)/,/g; print'` prints `1,234,567`.

## Checked

2026-11-02. Confirmed in perlre: lookaround syntax, `\K`, `\A`/`\z`/`\Z`, `\G`; perl5300delta/perl5360delta: variable-length lookbehind (maximum 255) added experimentally in 5.30 and mostly no longer experimental in 5.36; perl5220delta `\b{wb}`; perldiag for the two lookbehind errors. Removed: the unconfirmed version caveat and the CGI wording.

Method: documentation only; no commands were run.

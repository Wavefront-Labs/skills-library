---
id: computing-software.software-engineering.perl.transliteration-tr
name: transliteration-tr
category: computing-software
field: software-engineering
product: perl
tags: [perl, tr, transliteration, y-operator, perlop, transliteration-tr]
level: practitioner
status: docs-checked
description: "Count, map and delete characters with tr/// including ranges, the c, d, s, r flags and why variables do not interpolate."
sources: ["https://perldoc.perl.org/perlop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transliteration with tr///

**Goal:** fast character-level changes.

```perl
(my $up = $s) =~ tr/a-z/A-Z/;          # uppercase a copy (ASCII)
my $upper = $s =~ tr/a-z/A-Z/r;        # /r returns result (5.14+)
my $vowels = ($s =~ tr/aeiou//);       # count: empty replacement leaves text unchanged
$s =~ tr/a-zA-Z//cd;                   # delete everything that is not a letter
$s =~ tr/ //s;                         # squeeze runs of space to one
$s =~ tr/a-y/b-z/;                     # rot-1
$s =~ tr/\x{80}-\x{ff}//d;             # delete Latin-1 range
```

## Flags
`c` complement the search list; `d` delete found chars without a replacement; `s` squeeze duplicate output chars; `r` return the new string, leave the original (non-destructive).

## Rules
- `tr` returns the number of characters matched/replaced, and works on `$_` by default.
- No regex features: no classes, quantifiers or interpolation. `tr/$a/$b/` uses the literal characters `$`, `a`, `b`. To use variables: `eval "tr/$from/$to/"`, with the validation risks of string eval.
- If the replacement list is shorter, its last character is repeated (unless `/d`).
- `y///` is a synonym for `tr///`.
- On Unicode text `tr/a-z/A-Z/` only handles ASCII letters; use `uc`/`ucfirst` or `\U` for full case-mapping.

## Failure modes
- `tr/a-z//` in list/void context discards the count silently.

## Self-check
- [ ] `perl -e '$_="hello"; print tr/l//'` prints `2`.

## Checked

2026-11-02. Confirmed in perlop (Quote-like Operators, tr///): `c`, `d`, `s`, `r` flags, `y` synonym, return value is the count, no variable interpolation, replacement-list padding with the last character, ranges, `/r` from the 5.14 delta. Removed: the EBCDIC bullet and the read-only value claim.

Method: documentation only; no commands were run.

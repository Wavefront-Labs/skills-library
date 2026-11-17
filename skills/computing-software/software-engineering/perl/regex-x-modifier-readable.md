---
id: computing-software.software-engineering.perl.regex-x-modifier-readable
name: regex-x-modifier-readable
category: computing-software
field: software-engineering
product: perl
tags: [perl, free-spacing, xx-modifier, regex-style, perlre, regex-x-modifier-readable]
level: practitioner
status: docs-checked
description: "Write maintainable regexes with /x comments, /xx, Q..E, quotemeta and composition of qr// fragments."
sources: ["https://perldoc.perl.org/perlre", "https://perldoc.perl.org/perlretut"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Readable patterns with /x, /xx and qr//

**Goal:** regexes a colleague can review.

```perl
my $re = qr/
    ^ \s*
    (?<key>   [A-Za-z_]\w* )      # identifier
    \s* = \s*
    (?<value> "[^"]*" | \S+ )     # quoted or bare
    \s* (?: \# .* )? $            # optional comment (# must be escaped under /x)
/x;
my $date  = qr/(\d{4})-(\d\d)-(\d\d)/;
my $stamp = qr/$date T (\d\d):(\d\d)/x;   # compose
```

## Details
- Under `/x` whitespace and `#` comments are ignored; match a literal space with `\ ` or `[ ]`, a literal `#` with `\#`.
- `/xx` (5.26+) also ignores spaces and tabs inside bracketed classes: `[a-z A-Z]`.
- Metacharacters in variables: `/\Q$text\E/` or `quotemeta($text)`. Without it user input like `a.b(` changes the pattern or dies "Unmatched (".
- Precompile with `qr//` outside loops instead of interpolating a changing variable into a pattern.
- `qr/.../i` flags are embedded and stringify as `(?^i:...)`, so a `qr` object keeps its own flags when interpolated into another pattern.
- Alternation lists: build with `my $alt = join '|', map quotemeta, sort { length $b <=> length $a } @words;` (longest first, because alternation is ordered).
- Default flags can be set lexically with `use re '/flags'` (5.14+, see re).

## Failure modes
- A delimiter character inside a `/x` comment still ends the pattern.

## Self-check
- [ ] `perl -e 'print qr/a b/ix'` prints `(?^ix:a b)`.

## Checked

2026-11-02. Confirmed in perlre and perlop: `/x` whitespace and `#` comments, `/xx` (perl5260delta), `\Q..\E`, `qr//` stringification `(?^ix:...)` (perlre), `use re '/flags'` (perl5140delta, re). Removed: the (unconfirmed) caveat, the compile-caching bullet and the `eval` failure mode.

Method: documentation only; no commands were run.

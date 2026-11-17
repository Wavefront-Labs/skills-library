---
id: computing-software.software-engineering.perl.string-number-conversion
name: string-number-conversion
category: computing-software
field: software-engineering
product: perl
tags: [perl, numeric-strings, eq-versus-equals, perlop, looks-like-number, string-number-conversion]
level: practitioner
status: docs-checked
description: "Handle automatic string/number conversion safely: == versus eq, looks_like_number, numeric warnings and float formatting."
sources: ["https://perldoc.perl.org/perldata", "https://perldoc.perl.org/perlop", "https://perldoc.perl.org/perlnumber"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String and number conversion

**Goal:** avoid silent conversion bugs; Perl scalars are strings or numbers by operator.

## Operators choose the type
| Numeric | String |
|---|---|
| `== != < > <= >= <=>` | `eq ne lt gt le ge cmp` |
| `+ - * / % **` | `. x` |
```perl
"10" == 10.0;     # true
"10" eq "10.0";   # false
"abc" == 0;       # true, but warns "isn't numeric" under use warnings
"3abc" + 4;       # 7 with warning (leading digits parsed)
"1_000" + 0;      # 1 (underscores only in source literals)
"0x1A" + 0;       # 0; use hex("0x1A") or oct("0x1A")
```

## Validate input
```perl
use Scalar::Util qw(looks_like_number);
die "not a number: $in" unless looks_like_number($in);
```
`looks_like_number` is from Scalar::Util (see its documentation for exactly what it accepts); use a regex such as `/\A-?\d+\z/` for strict integers.

## Float traps
- `0.1 + 0.2 == 0.3` is false; compare with a tolerance `abs($a-$b) < 1e-9`, or use `Math::BigFloat`/integer cents.
- Binary floating point is inexact; round money with `sprintf('%.0f', $x)` or keep integer cents.
- `"10" + "20"` is 30, `"10" . "20"` is "1020"; `$x++` on "a9" is string increment ("b0").
- Sorting: `sort @n` is stringwise (10 before 9); use `sort { $a <=> $b } @n`.

## Self-check
- [ ] `perl -we 'print "abc"==0'` shows the warning; code under test never triggers it.
- [ ] Comparisons use the operator matching the intended type.

## Checked

2026-11-02. Confirmed in perlop (`<=>`/`cmp`, numeric versus string operators, `"0 but true"` exemption from numeric warnings) and perldata (truth rules). Removed: unconfirmed claims about `looks_like_number` accepting Inf/NaN/whitespace, the `ivsize` and 2**53/2**64 bullet, and `int(19.99*100)` figure.

Method: documentation only; no commands were run.

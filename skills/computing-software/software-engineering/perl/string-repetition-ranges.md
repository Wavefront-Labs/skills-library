---
id: computing-software.software-engineering.perl.string-repetition-ranges
name: string-repetition-ranges
category: computing-software
field: software-engineering
product: perl
tags: [perl, range-operator, string-increment, repetition-operator, flip-flop, perlop, string-repetition-ranges]
level: practitioner
status: docs-checked
description: "Use the dot, x, .. and ++ operators including list repetition, string ranges, magic string increment and flip-flop."
sources: ["https://perldoc.perl.org/perlop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String, repetition, range and increment operators

**Goal:** know the less obvious operators.

```perl
my $line = '=' x 40;               # string repetition
my @zeros = (0) x 10;              # list repetition (parens!)
my @grid = map { [ (0) x 3 ] } 1..3;  # fresh rows; [ (0) x 3 ] x 3 would share
my $s = "a" . "b";  $s .= "c";
my @r = ('a'..'e');                # a b c d e
my @h = ('aa'..'ad');              # aa ab ac ad
my @d = reverse 1..5;
my $v = "az"; $v++;                # "ba"
$v = "Zz"; $v++;                   # "AAa"
$v = "a9"; $v++;                   # "b0"
$v = "9z"; $v++ ;                  # numeric 10 (not matching /^[a-zA-Z]*[0-9]*\z/)
```

## Flip-flop (scalar `..`)
```perl
while (<$fh>) { print if /BEGIN/ .. /END/; }    # inclusive range of lines
print if /BEGIN/ ... /END/;                    # '...' does not test END on the same line as BEGIN
print if 3 .. 5;                               # compares to $. (line number)
```

## Gotchas
- `..` in list context with non-numeric strings uses the magic increment: `'a'..'zz'` goes a, b ... z, aa ... zz; a bad end value yields everything up to the length of the end string.
- `x` with a negative count gives an empty result.
- `.` has equal precedence with `+`: `print "n=" . $a + $b` adds after concatenation; parenthesise.
- `undef` is treated as numeric by `++` and becomes 0 before incrementing; `--` is not magical (perlop).

## Self-check
- [ ] `perl -e '$v="Az";$v++;print $v'` prints `Ba`.

## Checked

2026-11-02. Confirmed in perlop: `x` list repetition and empty result for zero or negative counts, magic string increment rules and examples (`Az` to `Ba`, `zz` to `aaa`, pattern `/^[a-zA-Z]*[0-9]*\z/`), string range magic increment, flip-flop `..`/`...` with `$.`. Removed unverified: `.` versus `+` precedence example wording kept (table), `--` and `foreach` range laziness bullets.

Method: documentation only; no commands were run.

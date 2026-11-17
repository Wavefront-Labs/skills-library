---
id: computing-software.software-engineering.perl.undef-defined-truthiness
name: undef-defined-truthiness
category: computing-software
field: software-engineering
product: perl
tags: [perl, undef, defined, truthiness, perldata, undef-defined-truthiness]
level: intro
status: docs-checked
description: "Test for undef, empty and false values correctly: defined, length, exists, and the five false scalar values."
sources: ["https://perldoc.perl.org/perldata", "https://perldoc.perl.org/perlsyn", "https://perldoc.perl.org/perlop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# undef, defined and truthiness

**Goal:** pick the right test for 'missing', 'empty' and 'false'.

## What is false
Perl false scalars: `undef`, the empty string `""`, the number `0` and the string `"0"` (perldata); every other scalar is true, so `"00"` and `"0.0"` are true. An empty array or hash is false in boolean context.

```perl
if (defined $x)        { ... }  # has a value (maybe 0 or "")
if (length $s)         { ... }  # non-empty string (length undef is undef; test defined first)
if ($s)                { ... }  # false for "" and "0" - wrong for "0" input
my $v = $opt // 'default';      # defined-or: only undef triggers default
my $w = $opt || 'default';      # also replaces 0 and "" - often a bug
$h{k} //= 0;                    # init only if undef
```

## Gotchas
- `defined @array` and `defined %hash` are fatal errors since 5.22; test `if (@array)` instead.
- `exists $h{k}` asks whether the key is present; a key can exist with an undef value.
- `undef $x` clears a variable; `$x = undef` assigns; `undef @a` frees storage; `undef` as a list element of `my (undef, $b) = @_` discards.
- `use warnings` reports "Use of uninitialized value" only when an undef is used in an operation; under `no warnings` it silently becomes 0 or "".
- The special string `"0 but true"` is true yet exempt from numeric warnings (perlfunc).
- Numeric `==` on non-numeric strings warns and treats them as 0.

## Self-check
- [ ] `perl -we 'my $v=0; print $v // "d"; print $v || "d"'` prints `0d`.
- [ ] Defaults for optional args use `//` unless 0/"" are invalid.

## Checked

2026-11-02. Confirmed in perldata (false values `undef`, `""`, `0`, `"0"`) and perl5220delta (`defined(@array)` and `defined(%hash)` are fatal errors), perlfunc (`length undef` is undef, `"0 but true"` exempt from numeric warning), perldiag. FIXED: the self-described `"0E0"` DBI idiom and the `length` warning aside were not in the pages read and were removed; the false-values sentence is rewritten.

Method: documentation only; no commands were run.

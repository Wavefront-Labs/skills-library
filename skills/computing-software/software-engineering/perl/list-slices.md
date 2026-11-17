---
id: computing-software.software-engineering.perl.list-slices
name: list-slices
category: computing-software
field: software-engineering
product: perl
tags: [perl, slice, array-slice, list-slice, perldata, list-slices]
level: practitioner
status: docs-checked
description: "Use array slices, list slices, negative indices and ranges to select and assign multiple elements at once."
sources: ["https://perldoc.perl.org/perldata"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Array and list slices

**Goal:** pick several elements at once without loops.

```perl
my @a = qw(a b c d e);
my @mid  = @a[1..3];          # b c d
my @ends = @a[0, -1];         # a e
@a[0,1] = @a[1,0];            # swap without temp
my ($x, $y) = @a[2,3];
my @tail = @a[1..$#a];        # all but first

# list slice: parenthesise the list, then subscript it
my ($user, $host) = (split /@/, $email)[0, 1];
my $month = (localtime)[4];
my $first = (sort @a)[0];
my @two = (1,2,3)[5,6];       # two undefs: indexes out of range on a non-empty list

# slice of an array reference
my @s = @{$ref}[1,2];  my @t = $ref->@[1,2];   # postfix deref (5.24+)
```

## Gotchas
- `@a[1]` is a one-element slice (warns "Scalar value @a[1] better written as $a[1]"); you want `$a[1]`.
- A list slice needs the parentheses: `my $x = split(...)[0]` is a syntax error; use `(split ...)[0]`.
- A list slice of an empty list is empty, so `my ($m) = (undef_list)[0]` leaves `$m` undef.
- Slice assignment with too few right-hand values pads with undef.
- Ranges: `1..$n` is empty when `$n < 1`; `reverse 0..$#a` iterates backwards.

## Self-check
- [ ] `perl -e '@a=qw(a b c); print join ",", @a[-2,-1]'` prints `b,c`.

## Checked

2026-11-02. Confirmed in perldata: list slices need parentheses, a slice of an empty list is empty, and a slice of a non-empty list with out-of-range indices returns undef for each (`(@d)[8,9]` has two elements). FIXED: the example claimed `(1,2,3)[5,6]` is an empty list. Confirmed the `Scalar value @a[1] better written` warning (perldiag) and postfix slices (perlref). Removed the autovivification bullet.

Method: documentation only; no commands were run.

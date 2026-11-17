---
id: computing-software.software-engineering.perl.sorting-complex-schwartzian
name: sorting-complex-schwartzian
category: computing-software
field: software-engineering
product: perl
tags: [perl, sort, schwartzian-transform, sort-numeric, stable-sort, sort-by-multiple-keys, sorting-complex-schwartzian]
level: practitioner
status: docs-checked
description: "Sort by multiple keys, descending, case-insensitively and expensive keys using sort blocks and the Schwartzian transform."
sources: ["https://perldoc.perl.org/perlfunc", "https://perldoc.perl.org/sort"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sorting complex data

**Goal:** correct, efficient ordering.

```perl
my @n  = sort { $a <=> $b } @nums;             # numeric ascending
my @d  = sort { $b <=> $a } @nums;             # descending
my @s  = sort { lc($a) cmp lc($b) } @words;    # case-insensitive (ASCII); use fc under Unicode
my @r  = sort { $a->{last} cmp $b->{last} || $a->{first} cmp $b->{first} || $a->{age} <=> $b->{age} } @people;
my @byv = sort { $h{$b} <=> $h{$a} || $a cmp $b } keys %h;   # by value desc, tie-break key
my @rev = reverse sort @x;
```

## Schwartzian transform (cache an expensive key)
```perl
my @sorted = map  { $_->[1] }
             sort { $a->[0] <=> $b->[0] }
             map  { [ expensive($_), $_ ] } @items;
```

## Rules
- Default `sort` is string comparison: `sort 1, 10, 9` gives 1 10 9.
- `$a` and `$b` are package globals aliased to elements; never declare them with `my`, and do not modify them.
- The comparator must be consistent (return negative, zero, positive); `sort { $a > $b }` is wrong (returns 0 or 1).
- `sort` has been stable since v5.8.0 (perlfunc); `use sort 'stable'` is now a no-op.
- Sorting by a sub: `sort by_name @list` or `sort $subref @list`; a sub with the `($$)` prototype receives the two elements in `@_`.

## Self-check
- [ ] `perl -e 'print join ",", sort { $a <=> $b } 10,9,100'` prints `9,10,100`.

## Checked

2026-11-02. Confirmed in perlfunc `sort`: default string order, `$a`/`$b` globals, comparator sub, `($$)` prototype for sub names, sorting is stable since 5.8; sort pragma docs: the pragma is now a no-op. Removed: Sort::Key, List::UtilsBy, Unicode::Collate and NaN bullets, which the pages read do not cover.

Method: documentation only; no commands were run.

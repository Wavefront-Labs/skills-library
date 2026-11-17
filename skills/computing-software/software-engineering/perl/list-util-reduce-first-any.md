---
id: computing-software.software-engineering.perl.list-util-reduce-first-any
name: list-util-reduce-first-any
category: computing-software
field: software-engineering
product: perl
tags: [perl, list-util, reduce, first-any-all, sum-min-max, uniq-shuffle, list-util-reduce-first-any, perl-list-scalar-utils]
level: practitioner
status: docs-checked
description: "Use core List::Util: sum, sum0, min, max, first, any, all, none, reduce, uniq, shuffle, pairs and pairmap."
sources: ["https://perldoc.perl.org/List::Util"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# List::Util functions

**Goal:** replace hand-written loops with core helpers.

```perl
use List::Util qw(sum sum0 min max minstr maxstr first any all none notall reduce reductions
                  shuffle sample uniq uniqnum uniqint pairs unpairs pairkeys pairvalues pairmap pairgrep head tail zip mesh product);
my $total = sum(@n) // 0;               # sum of empty list is undef; sum0 returns 0
my $max   = max(@n);   my $min = min(@n);
my $f     = first { $_->{id} == $id } @records;     # first matching element or undef
print "ok" if any { $_ eq 'x' } @l;     # all, none, notall too
my $longest = reduce { length($a) >= length($b) ? $a : $b } @words;     # $a, $b are the accumulators
my @u = uniq @l;                        # first occurrences, order kept (undef is distinct from '')
my @sh = shuffle @l;
my %h = (a => 1, b => 2);
my @p = pairs %h;                       # [k, v] pairs: $_->key, $_->value
my @doubled = pairmap { ($a => $b * 2) } %h;
my @pairs = zip \@x, \@y;               # zip/mesh need List::Util 1.56 or later
```

## Rules
- Later functions depend on the List::Util version bundled with your Perl; the documentation gives "Since version" notes (`pairs` 1.29, `uniq` 1.45, `head` and `tail` 1.50, `zip` and `mesh` 1.56).
- `first`, `any`, etc. use `$_`; `reduce` uses package vars `$a`/`$b`: do not declare them with `my`.
- `sum`, `max` etc. return undef on an empty list: handle explicitly.
- `reduce` with one element returns it without calling the block; with none returns undef.
- `shuffle` and `sample` use `rand` unless `$List::Util::RAND` is set to a code reference (since 1.54).
- `first { ... } @l` returns the element, not true/false, so a first element of `0` or `""` is a false-looking result: use `any`.

## Self-check
- [ ] `perl -MList::Util=sum0,first -e 'print sum0(), first { $_ > 2 } 1..5'` prints `03`.

## Checked
2026-11-03: confirmed against the List::Util documentation (reduce, reductions, first, any, all, none, notall, min, max, minstr, maxstr, sum returning undef and sum0 returning 0, product, uniq, uniqnum, uniqint, shuffle, sample, pairs, unpairs, pairkeys, pairvalues, pairmap, pairgrep, head, tail, zip, mesh, $RAND, and the Since version notes). Fixed: uniq treats undef as distinct from the empty string; zip and mesh come from List::Util 1.56, not Perl 5.40. Removed: core-since-5.8 claim, List::MoreUtils and related pointers.
Method: documentation only; no commands were run.

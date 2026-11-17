---
id: computing-software.software-engineering.perl.nested-data-autovivification
name: nested-data-autovivification
category: computing-software
field: software-engineering
product: perl
tags: [perl, autovivification, data-structures, hash-of-arrays, perldsc, perllol, nested-data-autovivification]
level: practitioner
status: docs-checked
description: "Build hashes of arrays, arrays of hashes and deep structures; understand autovivification and how to avoid creating keys."
sources: ["https://perldoc.perl.org/perldsc", "https://perldoc.perl.org/perllol", "https://perldoc.perl.org/perlref"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested data structures and autovivification

**Goal:** model records without surprises.

```perl
my %hoa; push @{ $hoa{$key} }, $val;           # hash of arrays (auto-creates the array)
my %hoh; $hoh{$a}{$b}++;                        # hash of hashes (counts)
my @aoh = ({n=>1}, {n=>2});  print $_->{n} for @aoh;
my @aoa = ([1,2],[3,4]);     print $aoa[1][0];
push $h->{list}->@*, $x;                       # postfix (5.24+); push on a ref directly was removed in 5.24
for my $k (sort keys %hoa) { say "$k: @{ $hoa{$k} }" }
```

## Autovivification
Using an undefined value as a reference in an lvalue (or even rvalue nested) context creates the container.
```perl
my %h;
my $x = $h{a}{b}{c};        # creates $h{a} and $h{a}{b} (but not c)
exists $h{x}{y};            # creates $h{x}
```
Avoid creating keys by testing step by step:
```perl
my $v = exists $h{a} && exists $h{a}{b} ? $h{a}{b} : undef;
my $v2 = ($h{a} // {})->{b};
```
The extra containers show up in `keys` and `exists` checks.

## Rules
- Iterate `@{$h{list} // []}` to tolerate absence.
- Plain `=` on a container copies only the top level.

## Self-check
- [ ] `perl -e '%h=(); $x=$h{a}{b}; print exists $h{a} ? "viv":"no"'` prints `viv`.

## Checked

2026-11-02. Confirmed in perlref (autovivification), perldsc/perllol style structures, perl5240delta (`push` on a reference removed; postfix deref `->@*`). Removed: the `no autovivification` pragma, Storable/Test::More/Test::Deep and Data::Dumper bullets, and the foreach-over-keys claim, none of which the pages read cover.

Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.perl.hash-exists-delete-each
name: hash-exists-delete-each
category: computing-software
field: software-engineering
product: perl
tags: [perl, hash, exists, delete, each, keys, values, hash-exists-delete-each, perl-hashes]
level: intro
status: docs-checked
description: "Test, delete and iterate hash entries correctly; understand each iterator state and exists versus defined."
sources: ["https://perldoc.perl.org/perldata", "https://perldoc.perl.org/perlfunc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# exists, delete, each and keys on hashes

**Goal:** the basic hash operations and their pitfalls.

```perl
my %h = (apple => 3, pear => 0, plum => undef);
exists $h{plum};            # true: key present
defined $h{plum};           # false: value undef
delete $h{pear};            # returns the removed value
my @gone = delete @h{qw(apple plum)};   # slice delete
my $n = keys %h;            # count (scalar context)
for my $k (sort keys %h)   { print "$k=$h{$k}\n" }
while (my ($k, $v) = each %h) { ... }   # unordered
my %inv = reverse %h;       # invert (values must be unique)
my %seen; my @uniq = grep { !$seen{$_}++ } @items;
if (%h) { ... }             # true when non-empty
```

## Pitfalls
- `exists $h{a}{b}` **autovivifies** `$h{a}` as a hash ref. Check `exists $h{a} && exists $h{a}{b}`.
- `each` keeps an iterator per hash: breaking out of a `while (each ...)` early leaves it mid-way; calling `keys %h` resets it. Do not add or delete keys while iterating (deleting the most recently returned key with `each` is the one safe case).
- `scalar(%h)` returns the key count in Perl 5.26+ (older versions returned a bucket string; do not rely on it for old Perls).
- Keys are always strings: `$h{1.0}` and `$h{"1"}` are the same key; refs as keys stringify to `HASH(0x...)`.
- `my %h = @list` with an odd number of elements warns "Odd number of elements".
- `delete local $h{k}` (5.12+) temporarily removes a key.

## Self-check
- [ ] `perl -we 'my %h; print exists $h{a}{b} ? 1:0; print exists $h{a} ? " viv":""'` prints `0 viv`.

## Checked

2026-11-02. Confirmed in perlfunc: `each` iterator reset by `keys`/`values`, deleting the most recently returned key is safe, scalar `keys`; perl5260delta for `scalar(%hash)`; perl5120delta for `delete local`; perlref for autovivification; perldiag for the odd-number warning. Removed: the FieldHash and CPAN pragma suggestions and the bareword/function key claim, which the pages read do not cover.

Method: documentation only; no commands were run.

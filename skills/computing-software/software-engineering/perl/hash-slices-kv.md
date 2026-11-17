---
id: computing-software.software-engineering.perl.hash-slices-kv
name: hash-slices-kv
category: computing-software
field: software-engineering
product: perl
tags: [perl, hash-slice, kv-slice, perldata, hash-slices-kv]
level: practitioner
status: docs-checked
description: "Use hash slices, key/value slices (%h{...}) and slice assignment for subsets, merging and defaults."
sources: ["https://perldoc.perl.org/perldata"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hash slices and key/value slices

**Goal:** operate on groups of keys at once.

```perl
my %h = (a=>1, b=>2, c=>3, d=>4);
my @vals = @h{qw(a b)};          # (1,2)
@h{qw(x y)} = (10, 20);          # assign several keys
my %sub  = map { $_ => $h{$_} } qw(a c);   # subset, any Perl
my %sub2 = %h{qw(a c)};          # key/value slice, 5.20+
my %idx  = %arr[0,1];            # index/value slice of an array (5.20+)
my %merged = (%defaults, %opts); # later keys win
@h{keys %o} = values %o;         # merge in place
delete @h{qw(a b)};              # slice delete
my ($host, $port) = @{$cfg}{qw(host port)};   # via ref
my ($h2, $p2)     = $cfg->@{qw(host port)};   # postfix, 5.24+
my %kv = $cfg->%{qw(host port)};              # postfix key/value slice
```

## Gotchas
- The sigil follows the result, not the container: `@h{...}` for a list of values, `%h{...}` for key/value pairs, `$h{k}` for one value.
- `%h{...}` key/value slices need Perl 5.20 or later (perl5200delta).
- Building a lookup set: `my %set; @set{@list} = ();` then `exists $set{$x}`.
- Options with defaults: `my %o = (size => 10, @_);` allows the caller to override but not validate; check unknown keys explicitly.

## Self-check
- [ ] `perl -e '%h=(a=>1,b=>2); %s=%h{"a"}; print join ",", %s'` prints `a,1`.

## Checked

2026-11-02. Confirmed: `%h{...}` and `%a[...]` key/value slices in perl5200delta, postfix `->@{}`/`->%{}` slices in perlref and perl5240delta (stable in 5.24). Removed: the claim that rvalue slices never create keys, which the pages read do not state.

Method: documentation only; no commands were run.

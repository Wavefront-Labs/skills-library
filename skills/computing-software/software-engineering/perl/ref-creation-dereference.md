---
id: computing-software.software-engineering.perl.ref-creation-dereference
name: ref-creation-dereference
category: computing-software
field: software-engineering
product: perl
tags: [perl, reference, dereference, postfix-deref, anonymous-array, perlref, ref-creation-dereference, perl-references]
level: intro
status: docs-checked
description: "Create references with backslash and anonymous constructors, dereference with arrows, blocks and postfix syntax."
sources: ["https://perldoc.perl.org/perlref", "https://perldoc.perl.org/perlreftut"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating and dereferencing references

**Goal:** the complete reference syntax.

```perl
my @a = (1,2,3); my %h = (k => 'v'); my $s = "x";
my ($ar, $hr, $sr, $cr) = (\@a, \%h, \$s, \&func);
my $anon_a = [1, 2, [3, 4]];
my $anon_h = { name => 'x', tags => [qw(a b)] };
my $anon_c = sub { return @_ };

# dereference (three equivalent styles)
@$ar;  @{$ar};  $ar->@*;          # whole array (postfix: 5.24+)
$$ar[0];  ${$ar}[0];  $ar->[0];   # element
%$hr;  $hr->%*;  $$hr{k};  $hr->{k};
$$sr;  $sr->$*;   $cr->(1,2);  &$cr(1,2);  &{$cr}(1,2);
$#{$ar};  $#$ar;  $ar->$#*;       # last index
scalar @$ar;      # count
@{$h->{list}}[0,1];  $h->{list}->@[0,1];   # slices
```

## Rules
- The arrow is optional between subscripts: `$d->{a}[0]{b}` is `$d->{a}->[0]->{b}`.
- `\(@a)` returns a list of refs to each element; `\@a` is one ref to the array. `[@a]` copies the array into a new anonymous one.
- A reference used as a boolean is true; used as a string is `ARRAY(0x...)`; used as a number is its address.
- `{ ... }` is ambiguous between block and hash constructor: use `+{ ... }` for a hash and `{; ... }` for a block when it matters, such as in `map`.
- Ref-to-ref: `$$rr` is the inner ref; `$$$rr` the value.
- Compare refs with `==` (numeric value is the address).
- Under `use strict 'refs'`, using a string as a reference ("symbolic reference") dies: `@{"name"}` fails; that is a feature.

## Failure modes
- A wrong-type dereference dies with a message such as `Not an ARRAY reference`; print `ref($x)` to see what you have.
- Copying a nested structure with `my @copy = @orig` shares the inner refs.
- `return \@local` is fine (the lexical lives on).

## Self-check
- [ ] `perl -e '$d={a=>[10,20]}; print $d->{a}[1], $d->{a}->$#*'` prints `201`.

## Checked

2026-11-02. Confirmed in perlref and perlreftut: backslash and anonymous constructors, the three deref styles, postfix `->@*`, `->%*`, `->$*`, `->$#*` (5.24 delta), optional arrow between subscripts, `\(@a)`, symbolic references under strict refs, the `+{`/`{;` disambiguation. Removed: `Scalar::Util::refaddr` comparison, the `return \$_[0]` aliasing and 'Not an ARRAY reference' wording.

Method: documentation only; no commands were run.

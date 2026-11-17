---
id: computing-software.software-engineering.perl.sub-args-aliasing
name: sub-args-aliasing
category: computing-software
field: software-engineering
product: perl
tags: [perl, sub-arguments, at-underscore, named-arguments, perlsub, sub-args-aliasing, perl-subroutines]
level: practitioner
status: docs-checked
description: "Unpack @_ safely, understand that @_ aliases the caller's variables, and pass named parameters."
sources: ["https://perldoc.perl.org/perlsub"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sub arguments, @_ aliasing and named parameters

**Goal:** write subs whose argument handling is predictable.

```perl
sub add { my ($x, $y) = @_; return $x + $y }
sub first { my $self = shift; my %o = (size => 10, @_); ... }
sub named { my ($args) = @_; my $n = $args->{name} // die "name required"; ... }
add(1, 2);  &add(1, 2);  my $f = \&add; $f->(1, 2);
```

## Aliasing
`@_` elements alias the caller's variables: `sub inc { $_[0]++ }  my $n = 1; inc($n);` makes `$n` 2. Copy with `my (...) = @_` unless aliasing is the point. Passing a literal then modifying `$_[0]` dies "Modification of a read-only value".

## Rules
- Arrays and hashes passed flat: `f(@a, @b)` arrives as one list. Pass references to keep them separate: `f(\@a, \@b)`.
- `&foo;` (no parens, with ampersand) calls with the caller's current `@_`; `&foo()` disables prototypes.
- Return value is the last evaluated expression; use explicit `return` for clarity. A sub ending in `if` can return the condition value unexpectedly.
- `return;` for failure (empty list / undef); `return wantarray ? @r : \@r;` only if documented.
- Validate named args: `my %o = (a => 1, @_); my @bad = grep { !/^(?:a|b)\z/ } keys %o; die "unknown: @bad" if @bad;`.
- Default positional values: `my $n = shift // 10;`.
- Recursion: call by name, or `__SUB__` with `use feature 'current_sub'` (5.16+).

## Failure modes
- `my $x = @_;` gives the count of arguments, not the first one.
- `my ($self) = shift;` still works but `my $self = shift;` is idiomatic.

## Self-check
- [ ] `perl -e 'sub i{$_[0]++} $n=1;i($n);print $n'` prints `2`.

## Checked

2026-11-02. Confirmed in perlsub: `@_` aliases arguments, `&foo;` shares `@_`, `&foo()` bypasses prototypes, last evaluated value is returned, `__SUB__` (perl5160delta, feature current_sub). Removed: the Params::Validate/Type::Params remark and unchecked cost claim.

Method: documentation only; no commands were run.

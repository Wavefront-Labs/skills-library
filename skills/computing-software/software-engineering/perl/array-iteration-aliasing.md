---
id: computing-software.software-engineering.perl.array-iteration-aliasing
name: array-iteration-aliasing
category: computing-software
field: software-engineering
product: perl
tags: [perl, foreach, aliasing, each-array, map-grep, perlsyn, array-iteration-aliasing]
level: practitioner
status: docs-checked
description: "Iterate with foreach, each @array and keys @array, and understand that $_ and loop variables alias elements."
sources: ["https://perldoc.perl.org/perlsyn", "https://perldoc.perl.org/perlfunc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Iterating arrays and aliasing

**Goal:** loop correctly and know when loops modify the original data.

```perl
for my $item (@list) { $item =~ s/^\s+//; }   # modifies @list elements: loop var is an alias
for my $i (0 .. $#list) { print "$i: $list[$i]\n" }
while (my ($i, $v) = each @list) { ... }       # each/keys/values on arrays: Perl 5.12 and later
for my $i (keys @list) { ... }

my @sq   = map  { $_ * $_ } @nums;       # transform
my @even = grep { $_ % 2 == 0 } @nums;   # filter
my $n    = grep { /x/ } @strs;           # count in scalar context
```

## Aliasing gotchas
- `map`/`grep`/`for` alias `$_` to the element: `s/x/y/ for @a;` edits `@a`; `map { s/x/y/; $_ } @a` also edits the original. Use `s/x/y/r` or copy first: `map { (my $c = $_) =~ s/x/y/; $c } @a`.
- Never `push`/`splice` the array you are iterating with `for`.
- `for my $x (@a, @b)` aliases elements of both.
- A hash-returning map needs a disambiguating `+{ ... }` or `{; ... }`, else Perl guesses block vs hashref: `map { $_ => 1 } @l` works; `map { "\L$_" => 1 }` is guessed as an expression/hash: write `map {; "\L$_" => 1 } @l`.
- Postfix form `print for @a;` uses `$_`; nested loops using `$_` clobber it; name the variable.
- Lexical loop variable `my $x` is scoped to the loop; an outer `$x` is restored afterwards.

## Self-check
- [ ] `perl -e '@a=(1,2);$_*=2 for @a;print "@a"'` prints `2 4`.

## Checked
2026-11-02: confirmed against perlsyn (foreach aliasing) and perlfunc (each, keys, values on arrays need Perl 5.12; map block versus hash constructor). Removed: read-only-literal and last/next-in-map remarks.
Method: documentation only; no commands were run.

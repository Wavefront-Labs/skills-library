---
id: computing-software.software-engineering.perl.closures-state-vars
name: closures-state-vars
category: computing-software
field: software-engineering
product: perl
tags: [perl, closure, state-variable, lexical-sub, my-sub, perlsub, closures-state-vars]
level: practitioner
status: docs-checked
description: "Build closures over lexicals, use state for persistent variables, and use lexical subs; avoid shared-variable warnings."
sources: ["https://perldoc.perl.org/perlsub", "https://perldoc.perl.org/perlref"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Closures, state variables and lexical subs

**Goal:** keep private state without globals.

## Closures
```perl
sub make_counter { my $n = shift // 0; return sub { return $n++ } }
my ($c1, $c2) = (make_counter(), make_counter(5));
$c1->(); $c1->();   # 0, 1  ($c2 has its own $n)
my @subs = map { my $i = $_; sub { $i * 2 } } 1..3;   # each closure has its own $i
```

## state
```perl
use feature 'state';              # or use v5.10 or higher
sub next_id { state $id = 0; return ++$id }
sub seen    { state %seen; return $seen{ $_[0] }++ }
```


## Lexical subs
`my sub helper { ... }` (experimental before Perl 5.26) is lexically scoped to the enclosing block: handy for private helpers. `__SUB__` (feature `current_sub`) allows anonymous recursion.

## Gotchas
- Named subs capture the first instance of an outer `my` only; Perl warns `Variable "$x" will not stay shared` for named subs nested in other subs. Use anonymous subs or pass arguments.
- Closures keep the captured variables alive: a closure that captures `$self` can create a reference cycle (see weak references).

## Self-check
- [ ] `perl -E 'sub c{my $n=0;sub{++$n}} $a=c();$b=c();$a->();say $a->(),$b->()'` prints `21`.

## Checked
2026-11-02: confirmed against perlsub (state variables need feature state or use v5.10; lexical subs stable from 5.26; __SUB__ under current_sub) and perlref (closures; "will not stay shared" warning for nested named subs). Removed: state-aggregate version note, per-closure state claim, my-$x-if-0 and string-eval remarks.
Method: documentation only; no commands were run.

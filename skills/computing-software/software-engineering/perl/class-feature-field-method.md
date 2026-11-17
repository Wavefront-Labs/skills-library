---
id: computing-software.software-engineering.perl.class-feature-field-method
name: class-feature-field-method
category: computing-software
field: software-engineering
product: perl
tags: [perl, feature-class, perlclass, core-oo, field-keyword, method-keyword, class-feature-field-method, perl-class-feature]
level: advanced
status: docs-checked
description: "Write classes with the core class feature (5.38+, experimental): class, field, method, :param and ADJUST."
sources: ["https://perldoc.perl.org/perlclass", "https://perldoc.perl.org/feature"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The class, field and method keywords

**Goal:** know the built-in object system and its experimental status.

```perl
use v5.38;
use feature 'class';
no warnings 'experimental::class';       # the class feature is experimental (perlclass)

class Point {
    field $x :param = 0;                 # constructor arg, default 0
    field $y :param = 0;
    field @history;                      # private state
    field $id = ++$Point::count;

    method coords { return ($x, $y) }
    method move($dx, $dy) {
        push @history, [$x, $y];
        $x += $dx; $y += $dy;
        return $self;                    # $self is automatic in methods
    }
    ADJUST { die "negative" if $x < 0 }  # runs after field init
}
class Point3D :isa(Point) {              # single inheritance only
    field $z :param //= 0;
}
my $p = Point->new(x => 1, y => 2);
$p->move(1, 1)->coords;
```

## Facts to check against your Perl
- The feature is still experimental and incomplete (perlclass). Later releases added attributes such as `:reader` and `:writer` and lexical `my method`; check perldelta for what your version supports.
- Fields are lexical variables visible within `method` and `ADJUST` blocks of the class.
- `:param` and `:param(name)` define constructor arguments.
- A class may inherit from one superclass (`:isa(Parent)`); roles are listed as still to be added (perlclass).
- `__CLASS__` gives the name of the class being constructed (usable in field initialisers).
- Enable it with `use feature 'class'`.

## Decision guide
Because the feature is experimental, weigh it against established CPAN object systems before using it in production.

## Self-check
- [ ] `perl -E 'use v5.38; use feature "class"; no warnings; class A { field $n :param; method n {$n} } say A->new(n=>3)->n'` prints `3`.

## Checked
2026-11-02: confirmed against perlclass (experimental status, field :param and :param(name), :isa single superclass, __CLASS__, ADJUST, roles not yet available) and feature (class). Removed: Perl-version attributions, opaque-object and unknown-argument claims, CPAN comparison.
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.perl.class-feature-adjust-attributes
name: class-feature-adjust-attributes
category: computing-software
field: software-engineering
product: perl
tags: [perl, adjust-block, object-pad, field-attributes, reader-attribute, class-feature-adjust-attributes]
level: sme
status: docs-checked
description: "Control construction order in the core class feature: field initialisers, ADJUST, inheritance, and migrating from Object::Pad."
sources: ["https://perldoc.perl.org/perlclass", "https://metacpan.org/pod/Object::Pad"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ADJUST blocks, field initialisation order and Object::Pad

**Goal:** predict construction order and migrate designs.

## Construction order (per perlclass)
- `ADJUST` blocks run in the order in which they are declared; fields can be initialised from `:param` constructor arguments, and an initialiser may use earlier fields (see perlclass for the full order).
```perl
class Counter {
    field $start :param = 0;
    field $n = $start;           # may use earlier field
    ADJUST { $n++ if $n < 0 }
    method next { ++$n }
}
```

## Attributes
- `field $x :param;` required parameter (dies if missing and no default).
- `field $x :param //= 10;` and `||= 10` defaults exist alongside `= 10` (`//=` applies if the value passed is undef, `||=` if it is false).
- `field $x :reader;` generates a getter (see perlclass for the Perl version that added it).
- Methods can be anonymous: `my $m = method { ... };` and called with `$obj->$m()`.

## Failure modes
- Because of the experimental status, semantics may change between releases; pin tests per Perl version.

## Self-check
- [ ] Tests run on each supported Perl; a file `use feature 'class'` without `no warnings 'experimental::class'` shows the experimental warning.

## Checked
2026-11-02: confirmed against perlclass (field :param defaults with =, //=, ||=; ADJUST order; :reader; anonymous methods; experimental status) and feature (class). Removed: full construction-order list, Object::Pad/Moo migration notes, version-specific compile errors.
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.perl.inheritance-mro-c3
name: inheritance-mro-c3
category: computing-software
field: software-engineering
product: perl
tags: [perl, inheritance, isa, use-parent, mro, c3, super, perlmro, inheritance-mro-c3]
level: advanced
status: docs-checked
description: "Set up inheritance with use parent, call SUPER::, and choose C3 method resolution with use mro 'c3' for multiple inheritance."
sources: ["https://perldoc.perl.org/perlobj", "https://perldoc.perl.org/perlmro", "https://perldoc.perl.org/mro"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inheritance, @ISA, SUPER and C3 method resolution

**Goal:** inherit predictably.

```perl
package Animal;  sub new { my $c = shift; bless {@_}, $c }  sub speak { 'noise' }
package Dog;
use parent -norequire, 'Animal';        # sets @ISA; -norequire when the class is in the same file
sub speak { my $s = shift; return 'Woof, not ' . $s->SUPER::speak() }
package main;
Dog->new->speak;
```
`use parent 'Animal';` (without `-norequire`) also `require`s `Animal.pm`. Older style: `our @ISA = ('Animal');`.

## Method resolution
- Default MRO is depth-first, left-to-right (DFS). With diamond inheritance DFS can call a shared base before the more specific class.
- `use mro 'c3';` in a class switches to C3 linearisation; then `$self->next::method(@_)` calls the next class in the C3 order, and `next::can`/`maybe::next::method` test for it.
- `mro::get_linear_isa('Dog')` shows the resolution order.
- `SUPER::` is resolved by the package of the code that contains the call, not the object's class.

## Rules
- `$obj->can('m')` returns a code ref; `$obj->isa('Class')` checks the inheritance chain; `DOES` defaults to `isa` and exists for role systems (perlobj).
- `AUTOLOAD` and `can` interplay: override `can` if AUTOLOAD provides methods.

## Failure modes
- Inheriting from a class you did not `use`/`require`.

## Self-check
- [ ] `perl -Mmro -e '@A::ISA=();@B::ISA=("A");print join ",", @{mro::get_linear_isa("B")}'` prints `B,A`.

## Checked
2026-11-03: confirmed against perlobj (use parent and -norequire, @ISA, SUPER resolved from the calling package, default depth-first MRO, use mro 'c3', can/isa/DOES, AUTOLOAD and can) and mro (next::method, next::can, maybe::next::method, mro::get_linear_isa, the diamond order D B C A). Removed: use base, role module names, the SUPER-in-roles advice, the method-cache claim, the error-message bullet and the mixed DFS/C3 claim.
Method: documentation only; no commands were run.

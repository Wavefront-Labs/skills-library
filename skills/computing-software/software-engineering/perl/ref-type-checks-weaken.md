---
id: computing-software.software-engineering.perl.ref-type-checks-weaken
name: ref-type-checks-weaken
category: computing-software
field: software-engineering
product: perl
tags: [perl, ref-function, reftype, blessed, weaken, circular-reference, scalar-util, ref-type-checks-weaken]
level: advanced
status: docs-checked
description: "Identify reference types with ref, reftype and blessed, and break reference cycles with Scalar::Util::weaken."
sources: ["https://perldoc.perl.org/perlref", "https://perldoc.perl.org/Scalar::Util"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reference types, blessed, and weak references

**Goal:** type-check references and avoid memory leaks from cycles.

```perl
use Scalar::Util qw(blessed reftype refaddr weaken isweak looks_like_number);
ref($x);          # '' (not a ref), 'ARRAY', 'HASH', 'CODE', 'SCALAR', 'REF', 'GLOB', 'Regexp', or a class name if blessed
reftype($x);      # underlying type even when blessed
blessed($x);      # class name or undef (safe on non-refs)
refaddr($x);      # numeric address (stable object id)
if (blessed($x) && $x->isa('My::Class')) { ... }
if (ref $x eq 'ARRAY') { ... }
```
Use `blessed($x) && $x->can('method')` rather than `ref($x) eq 'Foo'`, which breaks on subclasses. For error classes use `$@->isa(...)` after checking `blessed`.

## Cycles and weaken
Perl uses reference counting; two structures that point at each other are never freed until global destruction.
```perl
my $parent = { name => 'p' };
my $child  = { parent => $parent };
$parent->{child} = $child;
weaken($child->{parent});      # the back-pointer no longer counts
```
- `weaken` turns the reference into undef automatically when the target is freed; always check `defined` before use.
- `isweak($ref)` tests it. Copying a weak ref makes a strong copy.

## Failure modes
- Weakening the only reference frees the object immediately.

## Self-check
- [ ] `perl -MScalar::Util=weaken -e '$a={};$b={a=>$a};$a->{b}=$b;weaken $a->{b};'` leaves no cycle.

## Checked
2026-11-03: confirmed against perlref (ref return values, circular references and reference counting) and Scalar::Util (blessed, reftype, refaddr, weaken, isweak, weak references become undef, copies are strong). Removed: Devel::Cycle and Test::Memory::Cycle, the closure-cycle idiom and the constructor remark.
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.perl.operator-overloading-overload
name: operator-overloading-overload
category: computing-software
field: software-engineering
product: perl
tags: [perl, overload-pragma, operator-overloading, stringify-overload, fallback-overload, nomethod, operator-overloading-overload]
level: advanced
status: docs-checked
description: "Overload operators, stringification and comparison with use overload, including fallback, nomethod and copy constructors."
sources: ["https://perldoc.perl.org/overload"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator overloading with overload

**Goal:** objects that behave like values.

```perl
package Vec2;
use strict; use warnings;
use overload
    '+'   => \&add,
    '*'   => sub { my ($a, $k) = @_; Vec2->new($a->{x} * $k, $a->{y} * $k) },
    '=='  => sub { $_[0]{x} == $_[1]{x} && $_[0]{y} == $_[1]{y} },
    '""'  => sub { "($_[0]{x}, $_[0]{y})" },
    'bool'=> sub { 1 },
    fallback => 1;       # derive missing operators from the ones defined (via "" and 0+ conversions)
sub new { my ($c, $x, $y) = @_; bless { x => $x, y => $y }, $c }
sub add { Vec2->new($_[0]{x} + $_[1]{x}, $_[0]{y} + $_[1]{y}) }
```

## Rules
- The handler receives `($self, $other, $swapped)`; `$swapped` is true when the object was the right operand. Handle it for non-commutative operators (`-`, `/`, `<=>`, `cmp`, `.`).
- `fallback => undef` (default) tries autogeneration and dies if impossible; `fallback => 1` autogenerates and then falls back to normal Perl behaviour silently; `fallback => 0` disables autogeneration.
- With autogeneration enabled, a missing operator or conversion can be derived through the conversion operators `""`, `0+` and `bool`; define the ones whose derived behaviour would be wrong (overload, Magic Autogeneration).
- Mutators `+=` etc. use `+` unless `+=` is overloaded; implement `=` (copy constructor) when `++`/`+=` mutate in place and objects may be shared.
- `overload::StrVal($obj)` returns the string value without overloading; `overload::Overloaded($obj)` tests whether an object overloads anything.
- `use overload` is inherited by subclasses; method names can be given as strings to allow overriding.
- `<>` and `-X` overloads exist; `nomethod` catches any operator without a handler.
- Don't overload for cleverness: unexpected `+` semantics hurt readability.

## Self-check
- [ ] `print Vec2->new(1,2) + Vec2->new(3,4)` prints `(4, 6)` and `"$v" eq "(4, 6)"` holds.

## Checked
2026-11-03: confirmed against the overload documentation (handler arguments and the swapped flag, fallback undef/true/false semantics, nomethod, the -X key, copy constructor and mutators, overload::StrVal and overload::Overloaded, inheritance and method names given as strings). Removed: the example subtraction and comparison handlers (they called methods the snippet never defined), the fallback recommendation, the claim about hash keys, and overload::Method.
Method: documentation only; no commands were run.

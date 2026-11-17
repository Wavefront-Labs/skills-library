---
id: computing-software.software-engineering.crystal.splat-args
name: splat-args
category: computing-software
field: software-engineering
product: crystal
tags: [splat-args, splats-named-args, splat, variadic, tuple-splat, args-tuple, array-expansion, crystal]
level: practitioner
status: docs-checked
description: "Write variadic Crystal APIs with splat and double-splat parameters, named-only parameters and tuple splatting."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/splats_and_tuples.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/type_restrictions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Splat parameters and tuple expansion

Goal: write variadic APIs.

- `def sum(*elements)`: a splat parameter appears once, in any position; the arguments become a `Tuple` (e.g. `Tuple(Int32, Int32, Float64)`).
- Parameters after the splat are passed by name only; without a default they are required named parameters (`sum 1, 2, 3` is `missing argument: initial`). Methods with different required named parameters overload each other.
- A bare `*` means "named parameters follow": `def foo(x, y, *, z)`; `foo 1, 2, 3` is an arity error.
- Splat a Tuple at the call site with `*`: `foo *{1, 2}`; splat a NamedTuple with `**`.
- `**other` captures unmatched named arguments as a `NamedTuple`.
- Restrict elements: `*args : Int32` (all must match; the empty call matches no such overload) or `*args : _` (one or more of any type).
- When a method has a splat, named arguments cannot be used for positional parameters.

Verify: `crystal eval 'def f(*a) a.size end; p f(1,2,3)'`.

## Checked
Checked 2026-11-02 against the crystal-book Splats and tuples and Type restrictions pages. Removed: claims about splatting Arrays, `Tuple.from`, `to_a`, code bloat per arity.

Method: documentation only; no commands were run.

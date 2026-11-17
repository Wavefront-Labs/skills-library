---
id: computing-software.software-engineering.crystal.local-type-inference
name: local-type-inference
category: computing-software
field: software-engineering
product: crystal
tags: [local-type-inference, type-inference, inferred-type, typeof, local-variables, whole-program, crystal]
level: practitioner
status: docs-checked
description: "Predict local variable types in Crystal: reassignment, union after branches and block closures."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/local_variables.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/closures.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/type_restrictions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# How local type inference works

Goal: predict the type of any expression.

- A local variable's type is inferred from its usage, not only its initializer. Reassigning with a different expression gives it that expression's type from then on (`flower = "Tulip"` then `flower = 1` is an `Int32`).
- A variable assigned in a yielding block can be a union after it: `x = 1; foo { x = "hello" }` makes `x` `Int32 | String` until reassigned.
- If a proc closes over the variable, its type is the mix of all assignments to it.
- Methods are instantiated per argument type combination: every call with a different type combination is a different instantiation (`add true, false` fails with `undefined method '+' for Bool`).
- Type restrictions on parameters do not apply to the variables inside the method (`path = Path.new(path)` rebinds it to a `Path`).
- Instance variables follow separate rules (see instance-var-inference).

Verify: `crystal eval 'x = rand < 0.5 ? 1 : "a"; puts typeof(x)'`.

## Checked
Checked 2026-11-02 against the crystal-book Local variables, Closures and Type restrictions pages. Removed: `typeof`/`crystal tool context` usage claims, the empty-literal and nil-assignment gotchas, "whole-program inference".

Method: documentation only; no commands were run.

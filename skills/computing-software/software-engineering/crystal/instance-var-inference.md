---
id: computing-software.software-engineering.crystal.instance-var-inference
name: instance-var-inference
category: computing-software
field: software-engineering
product: crystal
tags: [instance-var-inference, type-inference, instance-variable, class-variable, nilable-ivar, ivar-inference, declare-type, crystal]
level: practitioner
status: docs-checked
description: "Predict Crystal instance and class variable type inference: the seven syntactic rules, nilable from partial init, and when to annotate."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/type_inference.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instance and class variable type inference

Goal: avoid surprising nilable ivars.

- Without an annotation, the compiler guesses from syntactic rules and takes the union of the types found. Rules apply to class variables too, and in methods other than `initialize`.
- Rules: (1) a literal; (2) `Type.new(...)`, also generic (`Array(Int32).new`); (3) a method parameter with a type restriction, including `initialize(@name : String)` (the compiler does not notice later reassignment of the parameter); (4) a class method with a return type restriction, or whose body the compiler can type by the earlier rules; (5) a parameter with a default value; (6) a `lib` function return; (7) an `out` lib argument. Also followed: `if`/ternary branches, `||` and `||=`, and constants.
- If an ivar is not assigned in all `initialize` methods, `Nil` is added: assigning only in `def lucky_number; @lucky_number = 42; end` gives `Int32 | Nil`. `@x ||= 42` is also `Int32 | Nil`, useful for lazy initialisation.
- Explicit restrictions: `@name : String`.
- When the compiler says it cannot infer the type, add an explicit type restriction.

Verify: build and read the exact error; add `: Type` and rebuild.

## Checked
Checked 2026-11-02 against the crystal-book Type inference page. Removed: `getter name : String` and class-variable declaration requirements, the `not_nil!` and `getter(x) { }` advice, the exact error wording and the require-order remark.

Method: documentation only; no commands were run.

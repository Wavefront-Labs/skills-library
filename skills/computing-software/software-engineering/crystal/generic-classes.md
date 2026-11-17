---
id: computing-software.software-engineering.crystal.generic-classes
name: generic-classes
category: computing-software
field: software-engineering
product: crystal
tags: [generic-classes, generics, generic-class, type-parameter, instantiate, splat-type-var, generic-struct, crystal]
level: practitioner
status: docs-checked
description: "Write generic classes, structs and modules in Crystal: inference, multiple and splat type variables, inheritance."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/generics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic classes and structs

Goal: write a reusable container.

```crystal
class MyBox(T)
  def initialize(@value : T); end
  def value; @value; end
end
MyBox(Int32).new(1)
MyBox.new(1)            # : MyBox(Int32), T inferred
MyBox(String).new(1)    # Error
```
- `Array`, `Hash`, `Set` and `Pointer` are generic. Several parameters are allowed (`MyDictionary(K, V)`) with any names.
- Type restrictions in a generic type's class methods become free variables, bound from the call's arguments; this works for `.new` (from `initialize`) and other class methods. A class method that needs `T` but cannot infer it is an error: give the type explicitly (`Foo(Int32).foo(1)`).
- Structs and modules can be generic; include a generic module with `include Moo(U)`.
- Inheritance: `class Int32Child < Parent(Int32)` or `class GenericChild(T) < Parent(T)`.
- Variadic: `class Foo(*T)` with `initialize(*@content : *T)`; `Foo(Int32, String)` or inferred from `Foo.new("Hello", 140)`. Zero arguments is `Parent().new`; plain `Parent.new` or `class Foo < Parent` (no arguments) is an error.

Verify: `crystal eval 'p typeof(MyBox.new(1))'` prints `MyBox(Int32)`.

## Checked
Checked 2026-11-02 against the crystal-book Generics page. Removed: the no-covariance claim, the binary-size remark, the `Pair`/`Cache` example names and the `Box(Int32 | String)` example.

Method: documentation only; no commands were run.

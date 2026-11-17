---
id: computing-software.software-engineering.crystal.generic-methods-restrictions
name: generic-methods-restrictions
category: computing-software
field: software-engineering
product: crystal
tags: [generic-methods-restrictions, generics, forall, free-variable, generic-method, type-restriction-generic, enumerable-of, crystal]
level: practitioner
status: docs-checked
description: "Write type-parametrised Crystal methods with forall free variables and type restrictions."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/type_restrictions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic methods, forall and restrictions

Goal: write type-parametrised functions.

```crystal
def foo(x : T) forall T
  T
end
foo(1)       # => Int32
def push(element : T, array : Array(T)) forall T
  array << element
end
push(4, [1, 2, 3])      # OK
push("oops", [1, 2, 3]) # Error
```
- `forall T` makes `T` the type used to instantiate the method; several free variables are allowed to match types across arguments.
- Extract a generic's argument: `x : Array(T)`. `foo([1, "a"])` gives `T` as `Int32 | String`.
- `x : T.class` accepts a type name rather than an instance (`foo(Int32)` gives `Array(Int32)` if the body returns `Array(T)`).
- Splats: `*x : *T` makes `T` a `Tuple` of all argument types (empty tuple for no arguments); `**x : **T` gives a `NamedTuple`; `Proc(*T, Int32)` extracts the argument types.
- `self` as a restriction means the type that finally owns the method (always the instance type, even in class methods); `self.class` restricts to the type.
- Restrictions do not apply to the variables inside the method.
- In general, prefer no restrictions except to define overloads: an unrestricted method still gives a compile error for bad types.

Verify: call with mismatched element types and read the error.

## Checked
Checked 2026-11-02 against the crystal-book Type restrictions page. Removed: the single-uppercase-name-as-constant claim, advice to constrain to `Indexable(T)`, the "no `T < Foo` bounds" claim, and `T.new`/`T::CONST` uses.

Method: documentation only; no commands were run.

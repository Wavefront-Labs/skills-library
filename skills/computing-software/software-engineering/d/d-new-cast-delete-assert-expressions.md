---
id: computing-software.software-engineering.d.d-new-cast-delete-assert-expressions
name: d-new-cast-delete-assert-expressions
category: computing-software
field: software-engineering
product: d
tags: [d-new-cast-delete-assert-expressions, expressions, new, cast, assert, import-expression, mixin-expression, downcast, d]
level: practitioner
status: draft
description: "Use new for classes/structs/arrays, the cast() family (qualifier casts, down-casts returning null), assert/throw as expressions and typeid/mixin/import expressions."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# new, cast, assert and other special expressions

Goal: use D's expression forms safely.

- `new Foo(args)`, `new int[](n)` zeroed array of n, `new int[3][2]`; `new S(1,2)` returns a pointer to a heap struct.
- `cast(Derived) base` returns null if the dynamic type does not match; `cast(const)`, `cast(immutable)`, `cast(shared)`, `cast()` strips top-level qualifiers.
- `assert(cond, "msg")`: throws `AssertError` (not an Exception) and is removed with `-release`; `assert(0)` is kept always as `halt`. Use `enforce` for runtime input checks.
- `import("file.txt")` reads a file at compile time (requires `-J<dir>`, dub `stringImportPaths`).
- `mixin("code")` compiles a string; `typeid(T)`; `throw` can appear in expressions (`x ? a : throw new Exception("x")`).
- Lambdas: `x => x * 2`, `(int a, int b) { return a + b; }`.
- `delete` is deprecated; use `destroy` plus `GC.free`.

Gotchas:
- `cast` to an unrelated qualifier hides bugs; limit to one function and mark `@trusted` after review.
- `assert(x)` side effects vanish in release builds.

Verify: unit test a failed downcast gives null and an assert failure raises `AssertError`.

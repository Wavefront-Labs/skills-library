---
id: computing-software.software-engineering.d.d-dip1000-return-scope-ref
name: d-dip1000-return-scope-ref
category: computing-software
field: software-engineering
product: d
tags: [d-dip1000-return-scope-ref, dip1000-scope, return-scope, return-ref, lifetime, escape-through-return, dip1000-return, d]
level: sme
status: docs-checked
description: "Declare that a result borrows from a parameter with return ref and return scope, including this and how the keywords combine."
sources:
  - https://dlang.org/spec/function.html
  - https://dlang.org/spec/attribute.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# return scope, return ref and lifetime relations

Goal: express that the result borrows from an argument.

- `ref int identity(return ref int x) { return x; }`: a `return ref` parameter ensures the returned reference does not outlive the matching argument; returning a reference to a local through it is an error.
- `int* balin(return scope int* p) { return p; }` (in `@safe` code): a `return scope` parameter with indirections can escape them only through the return value; assigning it to a global or passing it to a non-`scope` parameter that escapes is an error.
- Member functions: `return scope` applies to `this` of class and interface member functions, e.g. `C bofur() return scope { return this; }`; the attribute appears after the parameter list.
- For a `ref` parameter with both `return` and `scope`, it gets `return scope` semantics only if `return` and `scope` are adjacent in that order (`ref return scope v`); `return ref scope v` is `return ref`.
- Template functions, auto functions, nested functions and lambdas can deduce `return scope`.

Gotchas:
- Returning a plain `scope` parameter is an error (`return q; // error, cannot return 'scope' q`); use `return scope` to allow it.
- Escape analysis is only done in `@safe` code, with `-preview=dip1000` enabled.

Verify: in a `@safe` module under `-preview=dip1000`, check that storing the `return scope` result of `balin` in a global is rejected.

## Checked
Checked 2026-11-03 against the D spec Functions page (Return Ref Parameters, Scope Parameters, Return Scope Parameters, Ref Return Scope Parameters). Removed: the `first`/`get` array examples, the struct-pointer remark, the library-stability remark and the heap-copy advice (not on that page).

Method: documentation only; no commands were run.

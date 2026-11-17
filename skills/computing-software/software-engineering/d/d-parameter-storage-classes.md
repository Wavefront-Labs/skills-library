---
id: computing-software.software-engineering.d.d-parameter-storage-classes
name: d-parameter-storage-classes
category: computing-software
field: software-engineering
product: d
tags: [d-parameter-storage-classes, functions, in, out, ref, lazy, scope, return-ref, parameter-storage-class, default-arguments, d]
level: practitioner
status: docs-checked
description: "Choose parameter storage classes: in (const scope), out (reset to init), ref, lazy deferred evaluation, scope, return ref, plus default and named-style arguments."
sources:
  - https://dlang.org/spec/function.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parameter storage classes: in, out, ref, lazy, scope, return

Goal: express parameter intent.

- By value (default): copy of the argument. `ref`: alias to caller's lvalue. `out`: ref, set to `.init` on entry. `in`: behaves like `const` and `scope` (needs `-preview=in`); may bind lvalues and rvalues and may be passed by reference by the compiler.
- `lazy T x`: the argument is not evaluated before the call, only when (and each time) `x` is evaluated, so 0 or more times: `void log(lazy string msg) { if (on) writeln(msg); }`.
- `scope`: the parameter must not escape the call; `return`: it may be returned or copied to the first parameter.
- Defaults: `void f(int a, int b = 5)`; a default value is not inherited by overrides.
- Variadic: typesafe `void f(int[] a...)`, C-style `extern(C) void f(int n, ...)`, template `void f(T...)(T args)`.
- `auto ref T` accepts lvalues by ref and rvalues by value.
- Type constructors on parameters: `const`, `immutable`, `shared`, `inout`.

Gotchas:
- A `lazy` argument with side effects runs every read.
- Literals do not match `ref` or `out` parameters (use `auto ref` in templates, or `in`).

Verify: unittest counts evaluations of a lazy argument read twice.

## Checked

Date 2026-11-02. Confirmed in, out, ref, lazy, scope, return, auto ref, variadics and default arguments (Functions spec). Removed the unverified trailing-defaults claim and the lazy-as-delegate wording; corrected in, scope and return descriptions.

Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.d.d-ref-returns-and-delegates-closures
name: d-ref-returns-and-delegates-closures
category: computing-software
field: software-engineering
product: d
tags: [d-ref-returns-and-delegates-closures, functions, delegate, closure, function-pointer, lambda, ref-return, nested-function, callback, d]
level: practitioner
status: draft
description: "Return by ref, use function pointers vs delegates, lambdas, nested functions and closures capturing variables, with GC-allocated frames and static alternatives."
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

# ref returns, function pointers, delegates and closures

Goal: pass and return behaviour.

- `ref int at(ref int[] a, size_t i) { return a[i]; }` returns an lvalue; `auto ref` forwards lvalue-ness.
- Function pointer: `int function(int) fp = &f;` no context; delegate: `int delegate(int) dg = &obj.method;` or a lambda capturing locals.
- Nested functions access the enclosing locals; if a delegate to one escapes, the frame is allocated on the GC heap (closure). `@nogc` code cannot create escaping closures.
- Lambdas: `(a, b) => a + b`, `function (int x) => x` (no capture), `delegate`.
- Literal conversion: a lambda that captures nothing implicitly converts to function pointer; also use `toDelegate(fp)` from `std.functional`.
- `std.functional`: `partial`, `curry`, `compose`, `pipe`, `memoize`.

Gotchas:
- A delegate to a stack frame that is stored beyond the call without closure analysis (e.g. via `scope`) dangles.
- Loop variables captured in a delegate: each iteration gets a fresh variable for `foreach` but not for `for (int i...)`.

Verify: unittest creates counters from a function returning a delegate and checks independent state.

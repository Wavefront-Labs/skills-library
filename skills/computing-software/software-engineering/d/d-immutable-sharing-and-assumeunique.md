---
id: computing-software.software-engineering.d.d-immutable-sharing-and-assumeunique
name: d-immutable-sharing-and-assumeunique
category: computing-software
field: software-engineering
product: d
tags: [d-immutable-sharing-and-assumeunique, const-immutable, assumeunique, pure-factory, immutable-array, unique-reference, idup, d]
level: advanced
status: draft
description: "Create immutable arrays and objects: pure functions returning unique results, std.exception.assumeUnique, array literals, and shared/immutable data across threads."
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

# Building immutable data: assumeUnique, pure factories, immutable literals

Goal: produce `immutable` values without copies.

- A `pure` function whose parameters are immutable/const-only and returns mutable data yields a unique result that converts implicitly to immutable: `immutable int[] a = makeArr(5);`.
- Otherwise build mutable, then `auto s = assumeUnique(buf);` (from `std.exception`; nulls the source ref) after ensuring no other alias exists.
- `immutable(char)[]` from a char[]: `.idup`; from a Appender: `app.data.idup`.
- Message passing between threads requires immutable or `shared` data (`std.concurrency.send` checks for unshared mutable aliasing).
- Constants of aggregate type: `static immutable Foo f = Foo(1, 2);`.
- Immutable objects: `immutable c = new immutable(Cls)(args);` and `immutable` ctors.

Gotchas:
- `assumeUnique` is a promise; breaking it creates data races invisible to the compiler.
- `pure` strongly versus weakly: weakly pure functions with mutable params do not give unique results.

Verify: compile `immutable int[] x = f();` to confirm uniqueness inference.

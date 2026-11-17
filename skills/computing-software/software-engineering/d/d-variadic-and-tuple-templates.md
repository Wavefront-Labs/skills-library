---
id: computing-software.software-engineering.d.d-variadic-and-tuple-templates
name: d-variadic-and-tuple-templates
category: computing-software
field: software-engineering
product: d
tags: [d-variadic-and-tuple-templates, templates, variadic-template, tuple, aliasseq, staticmap, staticfilter, expression-tuple, type-sequence, d]
level: advanced
status: draft
description: "Use template parameter sequences (T...), AliasSeq, std.typecons Tuple, staticMap/Filter, compile-time indexing and slicing of type and value lists."
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

# Variadic templates, tuples and AliasSeq

Goal: process argument lists generically.

- `void log(Args...)(Args args) { foreach (a; args) write(a, " "); writeln(); }` : `args` is an expression tuple; `Args.length`, `args[0]`, `args[1 .. $]` are compile-time operations.
- `std.meta.AliasSeq!(int, string, 3)` makes a sequence of types/values/symbols; `staticMap!(F, seq)`, `Filter!(pred, seq)`, `staticIndexOf`, `Reverse`, `NoDuplicates`, `allSatisfy`, `anySatisfy`.
- Runtime tuple: `std.typecons.Tuple!(int, "id", string, "name")`, access `.id`, `t[0]`, `.expand`. D has no structured-binding syntax; use `t.expand` or index.
- `tuple(1, "a")` factory; `forward!args` from `std.functional` perfect-forwards with ref-ness (`auto ref` params).
- Unroll: `static foreach (i, T; Args) { ... }`.
- A `T...` can be a trailing parameter only.

Gotchas:
- A tuple declared as a variable (`auto x = tuple(...)`) vs a raw sequence differ; expression tuples cannot be stored in arrays.
- Sequences auto-flatten when nested.

Verify: `static assert(is(staticMap!(Unqual, const int, immutable long) == AliasSeq!(int, long)));`

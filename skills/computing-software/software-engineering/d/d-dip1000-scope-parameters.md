---
id: computing-software.software-engineering.d.d-dip1000-scope-parameters
name: d-dip1000-scope-parameters
category: computing-software
field: software-engineering
product: d
tags: [d-dip1000-scope-parameters, dip1000-scope, dip1000, scope, escape-analysis, scope-parameter, d]
level: advanced
status: docs-checked
description: "Use scope parameters so references cannot escape, with -preview=dip1000 escape analysis in @safe code."
sources:
  - https://dlang.org/spec/function.html
  - https://dlang.org/spec/expression.html
  - https://dlang.org/dmd-linux.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# scope parameters and -preview=dip1000

Goal: let @safe code take pointers/slices of stack data without escaping them.

- Enable with the dmd switch `-preview=dip1000`; `scope` escape analysis is only done in `@safe` functions, elsewhere the semantics must be enforced manually.
- `void thorin(scope int*)`: a `scope` parameter of reference type must not escape the call (assigned to a global, returned, or passed to a parameter that escapes it); it has no effect on non-reference types.
- `scope int[] a = [5, 6];` initialises a scope slice (requires `-preview=dip1000`).
- Because a `scope` argument cannot escape, the compiler may avoid heap-allocating an array literal, delegate literal or `new` expression passed to it, which can then be allowed in `@nogc` code (implementation defined).
- Spec examples of rejected code: `gp = q; // error, q escapes to global gp`, `gloin(q); // error, gloin() escapes q`, `return q; // error, cannot return 'scope' q`.

Gotchas:
- Class references count as pointers for `scope`: a `scope C q` parameter cannot be assigned to a global or returned.

Verify: write a function leaking a scope param to a global and confirm the compile error.

## Checked
Checked 2026-11-03 against the D spec Functions page (Scope Parameters, Return Scope Parameters), Expressions page (array literals, `-preview=dip1000`) and the dmd command-line page. Removed: the dub `dflags` line, the quoted compiler messages, the transitivity and inference remarks (not on those pages).

Method: documentation only; no commands were run.

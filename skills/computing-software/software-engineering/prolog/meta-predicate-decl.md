---
id: computing-software.software-engineering.prolog.meta-predicate-decl
name: meta-predicate-decl
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, meta-predicate-decl, module-transparent]
level: advanced
status: docs-checked
description: "Declare module-sensitive arguments with meta_predicate/1 specifiers 0 to 9, colon, caret and double slash."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/man/module.plx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# meta_predicate
```prolog
:- module(m, [twice/2, my_maplist/3]).
:- meta_predicate twice(0, -), my_maplist(2, ?, ?).
twice(G, done) :- call(G), call(G).
```
- Argument specs: `0..9` (a goal or closure taking that many extra arguments), `:` (module-sensitive term), `^` (goal with existential variables, as in `setof/3`), `//` (DCG body). `-`, `?`, `*` and `+` are not interpreted; they are documentation only.
- The system wraps each meta argument as `Module:Term` using the caller's context unless it is already qualified, so the goal resolves in the caller's module.
- `meta_predicate/1` is the portable mechanism; `module_transparent/1`, `context_module/1` and `strip_module/3` are the older, deprecated style.
## Gotchas
- Without the declaration, a goal passed into a module is resolved in the module that calls it, not where it came from.
- Expect `Module:Term` when inspecting a meta argument; use `strip_module/3` if needed.
## Self-check
Call `twice(writeln(hi), X)` from `user` with and without the declaration, with the goal defined only in `user`.

## Checked

2026-11-03. SWI-Prolog manual sections "Defining a meta-predicate" (specifiers 0..9, `:`, `^`, `//`, ignored `-`, `?`, `*`, `+`, Module:Term wrapping, maplist example) and the transparent-predicates section (module_transparent/1, context_module/1, strip_module/3 described as deprecated alternatives). Removed: claims about error messages and behaviour of undeclared predicates beyond context resolution.

Method: documentation only; no commands were run.

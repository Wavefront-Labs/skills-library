---
id: computing-software.software-engineering.nim.mixin-bind-symbol-resolution
name: mixin-bind-symbol-resolution
category: computing-software
field: software-engineering
product: nim
tags: [mixin-bind-symbol-resolution, generics, mixin, bind, open-symbol, closed-symbol, symbol-resolution, generic, nim]
level: sme
status: docs-checked
description: "Control when symbols in generic bodies are bound, using mixin for late-bound operators and bind for early binding."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mixin, bind and generic symbol lookup

Goal: make generic and template code pick up the right overloads.

- In generics there are "open" and "closed" symbols. A closed symbol cannot be re-bound in the instantiation context; an open one can. By default overloaded symbols are open and every other symbol is closed.
- Open symbols are looked up in two contexts: the definition and the instantiation. That is why the generic `==` for tuples finds an `==` for a `distinct` type defined after it.
- `mixin foo` forces a symbol to be open, for a name that has no overload visible at the definition, for example `mixin init` in `proc create*[T](): ref T`.
- `bind foo` is the counterpart: the identifier is looked up in the scope of the template or generic definition. It is rarely needed because definition-scope binding is the default.
- Both statements only make sense in templates and generics.
- Delegating bind: when `genericA` uses `mixin init` and is instantiated through `genericB` in a module that does not import the module defining `init`, instantiation fails with `undeclared identifier: 'init'`. Writing `bind init` inside `genericB` forwards the `init` visible in its module.

Gotchas:
- A symbol that has no overload at definition time stays closed until you write `mixin`.

Verify: a generic `create[T]()` that calls `init` compiles for a user type with `init` only after adding `mixin init`.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md from the Nim repository, "Symbol lookup in generics", mixin, bind and delegating bind sections read in full). Removed because the manual does not say them: the instruction to add `mixin $` for `$`, that method-call syntax is resolved after instantiation, and that the symbol set is "frozen" for non-dot calls. tut1 and lib were not read and were dropped from sources.
Method: documentation only; no commands were run.

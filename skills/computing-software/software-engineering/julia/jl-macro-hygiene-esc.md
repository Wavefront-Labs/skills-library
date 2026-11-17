---
id: computing-software.software-engineering.julia.jl-macro-hygiene-esc
name: jl-macro-hygiene-esc
category: computing-software
field: software-engineering
product: julia
tags: [julia, macro-hygiene-esc]
level: sme
status: docs-checked
description: "Write Julia macros with quote, interpolation, esc and gensym; inspect via @macroexpand."
sources: ["https://docs.julialang.org/en/v1/manual/metaprogramming/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Macros
- `macro twice(ex); quote $(esc(ex)); $(esc(ex)) end; end` splices the caller's expression into the caller's scope.
- Hygiene renames locals introduced by the macro; `esc` opts out. `gensym` makes unique names.
- Debug with `@macroexpand @twice f()`, `dump(:(x+1))`, `Meta.parse`.
- Prefer functions where they suffice; macros are expanded at parse time.
Verify: `@macroexpand` shows expected expression.

## Checked

2026-11-02. Confirmed against: Manual Metaprogramming page: quoting, macros, hygiene, esc, gensym, macroexpand, Meta.parse, dump. Removed: the claim that macros have no knowledge of types.
Method: documentation only; no commands were run.

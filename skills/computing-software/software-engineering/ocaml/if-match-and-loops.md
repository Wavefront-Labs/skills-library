---
id: computing-software.software-engineering.ocaml.if-match-and-loops
name: if-match-and-loops
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, if-match-loops, for-loop, while-loop, sequence-expression]
level: intro
status: docs-checked
description: "Write if/else, match, while and for as expressions: branch types must agree, sequencing with semicolons, and for-loop bounds."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# if, match, while, for

**Goal:** treat control flow as expressions with types.

```ocaml
let sign n = if n < 0 then -1 else if n = 0 then 0 else 1
let () = for i = 1 to 3 do print_int i done         (* inclusive: 1 2 3 *)
let () = for i = 3 downto 1 do print_int i done
let () = let i = ref 0 in while !i < 3 do incr i done
```

## Rules
- `if c then a else b`: both branches share a type. `if c then a` without else requires `a : unit`.
- `for` and `while` return `unit`; bounds of `for` are evaluated once and are inclusive.
- `e1; e2` evaluates `e1` (expected unit) then `e2`. A non-unit `e1` triggers warning 10 (non-unit statement).
- There is no `break`/`continue`: use recursion, a flag, or an exception (`exception Exit` is in Stdlib).

## Gotchas
- `if c then a; b else ...` is a syntax error. Parenthesise `(a; b)`.
- A nested `match` inside a match arm swallows following arms; wrap the inner match in parentheses or `begin ... end`.
- Prefer folds/recursion for loops that build values; `for` is for side effects.

## Self-check
- [ ] Every `if` without `else` has type unit.
- [ ] Inner matches are parenthesised.

## Checked
2026-11-02. Confirmed: if/for/while typing and for-loop semantics (manual expr), warning 10 (compiler warnings.ml). Removed: the dune dev-profile claim.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

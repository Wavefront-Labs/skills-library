---
id: computing-software.software-engineering.ocaml.let-bindings-and-shadowing
name: let-bindings-and-shadowing
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, let-bindings, ocaml-bindings, let-rec, shadowing, let-in]
level: intro
status: docs-checked
description: "Use let, let rec, let ... and and local let-in correctly, including shadowing and why top-level let is immutable."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Let bindings and shadowing

**Goal:** bind names correctly; know that `let` never mutates.

```ocaml
let x = 1                      (* top-level definition *)
let y = let t = x + 1 in t * 2 (* local, scope ends at 'in' *)
let rec fact n = if n <= 1 then 1 else n * fact (n - 1)
let rec even n = n = 0 || odd (n - 1)
and odd n = n <> 0 && even (n - 1)   (* mutual recursion needs 'and' *)
let a = 1 and b = 2                  (* 'and' bindings are simultaneous: b cannot see a *)
```

## Shadowing
`let x = 2` after `let x = 1` creates a new binding; earlier closures keep the old one.
Shadowing changes no value; use `ref` for mutable state (see references-and-mutability).

## Gotchas
- `let f x = ...` without `rec` cannot call itself; the error is "Unbound value f".
- A top-level `let () = ...` is the usual entry point; `let _ = expr` hides non-unit results.
- `let x = 1 in x; y` parses as `let x = 1 in (x; y)`; wrap in `begin ... end` or parentheses.

## Self-check
- [ ] Mutual recursion uses `let rec ... and ...`.
- [ ] The build shows no unused-variable warnings (26/27).

## Checked
2026-11-02. Confirmed: let/let rec/and syntax and scoping (manual expr/tutorial), warnings 26/27 (warnings.ml). Removed: dune dev-profile claim, `;;` usage.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

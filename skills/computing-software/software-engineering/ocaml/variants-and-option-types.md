---
id: computing-software.software-engineering.ocaml.variants-and-option-types
name: variants-and-option-types
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, variants-options, variant-types, constructors, option-type, inline-record]
level: intro
status: docs-checked
description: "Model alternatives with variants, inline records and option instead of null; exhaustive matching and constructor arguments."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variants and option

```ocaml
type shape = Circle of float | Rect of float * float | Point
type expr = Num of int | Add of expr * expr | Neg of expr
type msg = Move of { x : int; y : int } | Quit      (* inline record *)
let area = function Circle r -> 3.14159 *. r *. r | Rect (w, h) -> w *. h | Point -> 0.
let rec eval = function Num n -> n | Add (a, b) -> eval a + eval b | Neg e -> - eval e
```

## Notes
- `option` is `None | Some of 'a`; there is no null. Use `Option.map`, `Option.bind`, `Option.value ~default`, `Option.get` (raises `Invalid_argument`).
- `Circle of float * float` (two args) differs from `Circle of (float * float)` (one tuple arg).
- Inline records (`Move of {x; y}`) avoid a separate type, but the record cannot escape the constructor.
- The compiler warns on non-exhaustive matches (warning 8). Avoid catch-all `_` on types you will extend, so new constructors produce non-exhaustive warnings.

## Self-check
- [ ] Adding a constructor causes a compiler warning in every `match` over the type.

## Checked
2026-11-02. Confirmed: variant, inline record (cannot escape the binding), multi-argument vs tuple constructors (manual), Option.get raising Invalid_argument (option.mli). Removed: ppx_deriving remark.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

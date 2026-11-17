---
id: computing-software.software-engineering.ocaml.labelled-and-optional-arguments
name: labelled-and-optional-arguments
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, labelled-optional-args, labelled-arguments, optional-arguments, default-argument]
level: practitioner
status: docs-checked
description: "Declare ~label and ?optional arguments with defaults, apply them in any order, and avoid the optional-argument-before-positional trap."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/manual/api/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Labelled and optional arguments

```ocaml
let range ~start ~stop = List.init (stop - start) (fun i -> start + i)
let r = range ~stop:5 ~start:2
let greet ?(greeting = "Hello") name = greeting ^ ", " ^ name
let a = greet "Ann"            let b = greet ~greeting:"Hi" "Ann"
let opt ?x () = match x with Some v -> v | None -> 0     (* x : int option *)
let fwd ?x () = opt ?x ()      (* pass an option through with ?x *)
```

## Rules
- An optional argument must be followed by a positional (non-labelled) argument, otherwise it can never be omitted (warning 16 "unerasable optional argument").
- `~x` punning: `let f ~x = ...` and call `f ~x`.
- Full applications can reorder labels; partial applications with labels interact with inference, so annotate higher-order uses.
- Stdlib `ListLabels`, `ArrayLabels`, `StringLabels` give labelled versions (`ListLabels.fold_left ~f ~init l`).

## Self-check
- [ ] Every optional parameter is followed by a positional parameter, often `()`.

## Checked
2026-11-02. Confirmed: label and optional-argument syntax and defaults (manual expr/labels tutorial), warning 16, ListLabels. Fixed: `List.fold_left ~f ~init` (the labelled variant is ListLabels). Removed: label-commuting claim.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

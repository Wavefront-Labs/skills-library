---
id: computing-software.software-engineering.ocaml.parametric-polymorphism-and-inference
name: parametric-polymorphism-and-inference
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, parametric-polymorphism, ocaml-polymorphism, type-inference, type-variables, polymorphic-compare, type-annotation]
level: practitioner
status: docs-checked
description: "Read inferred types, use type annotations to localise errors, understand 'a variables, and polymorphic comparison and hashing."
sources: ["https://ocaml.org/manual/", "https://dev.realworldocaml.org/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parametric polymorphism and inference

```ocaml
let id x = x                         (* 'a -> 'a *)
let pair x y = (x, y)                (* 'a -> 'b -> 'a * 'b *)
let swap (a, b) : 'b * 'a = (b, a)
```

## Reading errors
- "This expression has type X but an expression was expected of type Y" points to where the mismatch was detected, not necessarily the bug. Annotate function parameters and results to move the error closer to the cause.
- `ocamlc -i file.ml` prints the inferred interface.
- `'_weak1` means a weak (not yet generalised) type; see value-restriction-and-weak-types.

## Polymorphic comparison
- `compare`, `=`, `Hashtbl.hash` work structurally on any type. They raise `Invalid_argument "compare: functional value"` on closures and may not terminate on cyclic data. Use `String.equal`, `Int.compare` in hot code and for Map/Set keys.

## Self-check
- [ ] Public functions have `.mli` signatures so inference is not the API.

## Checked
2026-11-02. Confirmed: `'_weak` types (manual polymorphism chapter), polymorphic compare raising on functional values and possible non-termination (stdlib.mli), `ocamlc -i`. Removed: ocamlfind and Merlin remarks.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

---
id: computing-software.software-engineering.ocaml.modules-structures-and-signatures
name: modules-structures-and-signatures
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, structures-signatures, ocaml-modules, mli-files, module-type, signature, abstract-type]
level: practitioner
status: docs-checked
description: "Organise code into modules, hide implementation with .mli files and module types, and use open/include safely."
sources: ["https://ocaml.org/manual/", "https://dev.realworldocaml.org/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modules, signatures, mli

Each `foo.ml` is module `Foo`; `foo.mli` is its interface.

```ocaml
(* stack.mli *)
type 'a t                       (* abstract *)
val empty : 'a t
val push : 'a -> 'a t -> 'a t
(* stack.ml *)
type 'a t = 'a list
let empty = []
let push x s = x :: s
```

```ocaml
module type ORD = sig type t val compare : t -> t -> int end
module Int_ord : ORD with type t = int = struct type t = int let compare = Int.compare end
```

## Notes
- Abstract types in `.mli` enforce invariants; `with type t = int` exposes the representation.
- A `.ml` value missing from the `.mli` is hidden; if unused it triggers warning 32 in the dev profile.

## Self-check
- [ ] Every library module has an `.mli` exposing only the intended API.

## Checked
2026-11-02. Confirmed: module/signature syntax, `with type`, abstract types (manual modules chapter and module tutorial), warning 32 (warnings.ml). Removed: doc-comment placement and dune library wrapping.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

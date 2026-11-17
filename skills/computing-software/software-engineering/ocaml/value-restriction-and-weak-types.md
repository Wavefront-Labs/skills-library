---
id: computing-software.software-engineering.ocaml.value-restriction-and-weak-types
name: value-restriction-and-weak-types
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, value-restriction, weak-type, eta-expansion, relaxed-value-restriction]
level: advanced
status: docs-checked
description: "Diagnose weak types ('_weak1) from partial applications and refs, and fix by eta-expansion or annotation."
sources: ["https://ocaml.org/manual/", "https://dev.realworldocaml.org/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Value restriction

```ocaml
let r = ref []                 (* '_weak1 list ref : not generalised *)
let f = List.map (fun x -> x)  (* '_weak2 list -> '_weak2 list *)
let f' l = List.map (fun x -> x) l   (* eta-expanded: 'a list -> 'a list *)
```

## Rules
- Only syntactic values (functions, constants, constructors of values) are generalised. Applications such as `ref []` or partial application are not, because they may hold mutable state.
- OCaml uses a relaxed value restriction: type variables in covariant positions can still be generalised.
- A weak type still unresolved at the end of a compilation unit without `.mli` is an error ("contains type variables that cannot be generalized").

## Fixes
1. Eta-expand: `let f l = ...`.
2. Annotate: `let r : int list ref = ref []`.
3. Write an `.mli` with the concrete type.
4. Wrap in a function that creates the ref: `let make () = ref []`.

## Self-check
- [ ] No `_weak` types in `ocamlc -i` output.

## Checked
2026-11-02. Confirmed: value restriction, relaxed value restriction, eta-expansion, weak variables at end of compilation unit (manual polymorphism chapter). Fixed: `ocamlfind ocamlc -i` to `ocamlc -i`.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

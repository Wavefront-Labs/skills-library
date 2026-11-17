---
id: computing-software.software-engineering.ocaml.polymorphic-equality-and-compare-pitfalls
name: polymorphic-equality-and-compare-pitfalls
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, polymorphic-equality, ocaml-equality-types, structural-equality, physical-equality, compare-function, hash-function]
level: practitioner
status: docs-checked
description: "Avoid pitfalls of = vs ==, compare on functional/cyclic/abstract values, NaN, and mutable records; define equal/compare/hash."
sources: ["https://ocaml.org/manual/api/", "https://ocaml.org/docs", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Equality and comparison

```ocaml
[1;2] = [1;2]         (* true: structural *)
[1;2] == [1;2]        (* false: physical *)
compare nan nan       (* 0: compare treats nan as equal to itself and less than other floats *)
nan = nan             (* false *)
```

## Pitfalls
- `=` on closures raises `Invalid_argument "compare: functional value"`.
- On cyclic structures, `=` may not terminate (`compare` too).
- `=` on abstract types compares internal representation, which breaks invariants (e.g. two equal sets with different tree shapes are `<>`): use `Set.equal`/`Map.equal`.
- Floats: use `Float.equal`/`Float.compare` for a total order; `Stdlib.compare` treats nan as equal to itself and smaller than any other float.

## Convention
Provide `equal`, `compare`, `hash` in each module and use them with `Map.Make`/`Hashtbl.Make`.

## Self-check
- [ ] No `=` on values containing functions or abstract data from other libraries.

## Checked
2026-11-02. Confirmed: =/==/compare semantics, functional values raise Invalid_argument, cyclic structures may not terminate, nan handling (stdlib.mli). Removed: Zarith, deriving and performance claims.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

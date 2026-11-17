---
id: computing-software.software-engineering.ocaml.references-and-mutability
name: references-and-mutability
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, references-mutability, ocaml-imperative, ref-cells, mutable-state, aliasing]
level: intro
status: docs-checked
description: "Use ref, :=, ! and incr, arrays and Bytes for mutation, and know when immutability is preferable and what is aliased."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/manual/api/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# References and mutability

```ocaml
let c = ref 0
let () = c := !c + 1; incr c            (* c is 2 *)
let a = Array.make 3 0
let () = a.(0) <- 5
let b = Bytes.of_string "abc"
let () = Bytes.set b 0 'X'              (* Bytes.to_string b = "Xbc" *)
```

## Notes
- `!` is dereference, not "not" (`not` is the boolean negation).
- `ref` is a record `{ mutable contents : 'a }`.
- `Array.make n (ref 0)` shares ONE ref among all slots; use `Array.init n (fun _ -> ref 0)`.
- Likewise `Array.make 3 (Array.make 3 0)` aliases one row; use `Array.make_matrix`.
- Arrays are bounds-checked (`Invalid_argument "index out of bounds"`) unless built with `-unsafe`.

## Self-check
- [ ] No `Array.make n (ref ...)` or `Array.make n (Array.make ...)` aliasing in your code.

## Checked
2026-11-02. Confirmed: `ref` as record with mutable contents, Array.make sharing of mutable element (array.mli), `-unsafe` disabling bounds checks (manual). Removed: fold-vs-ref advice.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

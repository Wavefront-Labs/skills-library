---
id: computing-software.software-engineering.ocaml.hashtbl-map-and-set
name: hashtbl-map-and-set
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, hashtbl-map-set, hashtbl, map-module, set-module, hash-functor]
level: practitioner
status: docs-checked
description: "Choose between mutable Hashtbl and immutable Map/Set, create functorial tables, and avoid polymorphic-hash pitfalls and mutation-during-iteration."
sources: ["https://ocaml.org/manual/api/", "https://ocaml.org/docs", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hashtbl, Map, Set

```ocaml
let h : (string, int) Hashtbl.t = Hashtbl.create 64
let () = Hashtbl.replace h "a" 1       (* replace: one binding; add: stacks bindings *)
let v = Hashtbl.find_opt h "a"
module SM = Map.Make (String)
let m = SM.add "a" 1 SM.empty
let n = SM.update "a" (function None -> Some 1 | Some x -> Some (x + 1)) m
module IS = Set.Make (Int)
```

## Notes
- `Hashtbl.add` shadows the previous binding of the same key (both remain); use `replace` for dictionary semantics.
- `Hashtbl.find` raises `Not_found`; prefer `find_opt`.
- The polymorphic `Hashtbl.hash` examines a limited number of meaningful nodes; for custom keys use `Hashtbl.Make (struct type t = ... let equal let hash end)`.
- The behaviour is not specified if a table is modified by `f` during `Hashtbl.iter`; collect keys first.
- Map/Set use the `compare` of the key module; `Map.of_list` is since 5.1.
- Concurrent accesses to a hash table must be synchronized (hashtbl.mli): guard with a `Mutex` or use per-domain tables.

## Self-check
- [ ] Concurrent access from multiple domains is protected.

## Checked
2026-11-02. Confirmed: add vs replace, find_opt, hash/Hashtbl.Make, iteration-while-modifying, synchronisation (hashtbl.mli), Map.of_list since 5.1 (map.mli). Removed: nothing substantive; reworded to the documented wording.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

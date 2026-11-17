---
id: computing-software.software-engineering.ocaml.lazy-values-and-seq
name: lazy-values-and-seq
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, lazy-evaluation, lazy-force, seq-module, lazy-streams]
level: practitioner
status: docs-checked
description: "Delay computation with lazy/Lazy.force and write lazy sequences with Seq; know exceptions and thread-safety caveats."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/manual/api/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lazy and Seq

```ocaml
let v = lazy (print_endline "computing"; 42)
let x = Lazy.force v + Lazy.force v     (* prints once *)
let rec nat n : int Seq.t = fun () -> Seq.Cons (n, nat (n + 1))
let first5 = nat 0 |> Seq.take 5 |> List.of_seq    (* Seq.take: OCaml 4.14+ *)
```

## Notes
- `Seq.t = unit -> 'a node`; `Seq.Nil` / `Seq.Cons (x, rest)`. Transformers such as `Seq.map f` are lazy.
- Seq is not memoised: calling `ys()` twice recomputes. `Seq.memoize` (4.14+) caches; `Seq.once` (4.14+) guards single use.
- A `lazy` that raises re-raises on every force. Forcing a lazy concurrently from several fibers, threads or domains raises `Lazy.Undefined` and is not concurrency-safe; add locks.
- `Hashtbl.to_seq`, `List.to_seq`, `String.to_seq`, `Seq.iter/fold_left` interoperate.

## Self-check
- [ ] A second `Lazy.force v` does not print "computing".

## Checked
2026-11-02. Confirmed: Lazy.force, re-raise on force, Undefined, concurrency note (lazy.mli); Seq type, take/memoize/once since 4.14, recomputation note (seq.mli).
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

---
id: computing-software.software-engineering.ocaml.containers-and-useful-libraries
name: containers-and-useful-libraries
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, container-libs, containers-library, logs, fmt, fpath, bos]
level: practitioner
status: docs-checked
description: "Use the Containers library (CCList, CCVector, CCHeap, CCIO, containers-data) to extend the OCaml standard library."
sources: ["https://github.com/c-cube/ocaml-containers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Containers

```ocaml
(* opam install containers ; libraries: containers *)
open CCList.Infix
let l = 1 -- 100
let firsts =
  l |> CCList.filter_map (fun x -> if x mod 3 = 0 then Some (float x) else None)
    |> CCList.take 5                        (* [3.; 6.; 9.; 12.; 15.] *)
```

## Notes
- Containers is an extension of the OCaml standard library (BSD licence) focused on data structures, combinators and iterators, with no dependency on unix, str or num. Every module is independent and prefixed `CC`; `CCList` provides safe `map`/`fold_right`/`append` and more.
- `open Containers` brings enhanced versions of the standard modules into scope; operators become monomorphic by default (use `Stdlib.(=)` or `open Stdlib` to restore polymorphic ones).
- Core modules include `CCVector` (resizable array with read-only/read-write mutability parameter), `CCHeap` (functional priority queue functorised over a `leq` order), `CCResult`, `CCSexp`, `CCByte_buffer` and `CCIO` (`with_in`, `with_out`, `read_lines_l`, `write_lines_l`; the resource must not escape `with_resource`).
- Sub-libraries: `containers.unix`, `containers.bencode`, `containers.cbor`, `containers.scc`. Since 3.0 the extra data structures (e.g. `CCFQueue`) live in the separate package `containers-data`, and `CCSexp` is in `containers` itself.
- Common types: `gen` is `unit -> 'a option`, `iter` is `(unit -> 'a) -> unit` (formerly `sequence`), `printer` is `Format.formatter -> 'a -> unit`.
- Containers-thread was removed in favour of Moonpool.
- For logging, formatting and time libraries, see the dedicated skills; this page does not cover them.

## Self-check
- [ ] `CCList.take 5` on the filtered list returns the first five multiples of 3 as floats.

## Checked

2026-11-08. Read in full: the ocaml-containers README (summary, 3.0 migration notes, monomorphic operators, tutorial).
Removed: the library table for fmt, logs, fpath, bos, astring, uri, ptime, mtime, timedesc, zarith, ocamlgraph and the Logs code sample (none covered by the cited page); ocaml.org and Jane Street landing sources.
Method: documentation only; no commands were run.

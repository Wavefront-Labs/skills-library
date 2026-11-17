---
id: computing-software.software-engineering.ocaml.weak-pointers-ephemerons-finalisers
name: weak-pointers-ephemerons-finalisers
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, weak-ephemerons-finalise, weak-pointers, ephemeron, gc-finalise]
level: advanced
status: docs-checked
description: "Use Weak arrays, Ephemeron tables and Gc.finalise for caches and resource cleanup, and understand their limits."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/manual/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Weak, Ephemeron, finalisers

```ocaml
module W = Weak.Make (struct type t = string let equal = String.equal let hash = Hashtbl.hash end)
let tbl = W.create 16
let s = W.merge tbl "shared-string"           (* hash-consing *)
module E = Ephemeron.K1.Make (struct type t = string let equal = String.equal let hash = Hashtbl.hash end)
let () = Gc.finalise (fun r -> print_endline "collected") (ref 0)
```

## Notes
- Weak references do not keep values alive; a `Weak.get` returns `None` after collection.
- Ephemeron keys behave like weak pointers; the data is kept alive by the GC only while all full keys are alive, and is emptied when a key is no longer alive.
- `Gc.finalise f v` registers `f` to be called with `v` at some point between the first time `v` becomes unreachable and the time it is collected; `v` must be heap-allocated. Do not rely on finalisers for correctness (close files with `Fun.protect`).
- Use `Gc.finalise_last` when you do not need the value.

## Self-check
- [ ] Resources like file descriptors are closed explicitly, not via finalisers.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the Weak, Ephemeron and Gc API pages (Weak.Make, create, merge; Ephemeron.K1.Make and liveness rules; Gc.finalise and finalise_last).

Removed or corrected: the claim that finalisers can run at any allocation point and the statement about constants and static data (the manual only says the value must be heap-allocated).

Method: documentation only; no commands were run.

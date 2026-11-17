---
id: computing-software.software-engineering.ocaml.queues-stacks-heaps-and-mutable-structures
name: queues-stacks-heaps-and-mutable-structures
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, data-structure-libs, queue-module, stack-module, priority-queue, dynarray]
level: practitioner
status: docs-checked
description: "Use Stdlib Queue, Stack, Dynarray (5.2) and community heaps; implement priority queues with Map or a binary heap."
sources: ["https://ocaml.org/manual/api/", "https://ocaml.org/docs", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queues, stacks, heaps

```ocaml
let q = Queue.create ()   let () = Queue.add 1 q; ignore (Queue.take_opt q)
let s = Stack.create ()   let () = Stack.push 1 s; ignore (Stack.pop_opt s)
(* Dynarray (OCaml 5.2+) *)
let d = Dynarray.create ()   let () = Dynarray.add_last d 1
```

## Notes
- `Queue`/`Stack` are mutable; use `take_opt`/`pop_opt` (since 4.08) to avoid `Queue.Empty`/`Stack.Empty`.
- `Dynarray` (growable array) is in the Stdlib since 5.2.

## Self-check
- [ ] A queue of 1e6 elements runs in linear time.

## Checked
2026-11-02. Confirmed: Queue/Stack take_opt/pop_opt since 4.08, Dynarray since 5.2 (queue.mli, stack.mli, dynarray.mli). Removed: third-party library recommendations and the no-heap claim.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

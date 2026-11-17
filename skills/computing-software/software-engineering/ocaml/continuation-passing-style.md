---
id: computing-software.software-engineering.ocaml.continuation-passing-style
name: continuation-passing-style
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, cps-continuations, cps, continuation-passing, trampoline, defunctionalization]
level: advanced
status: draft
description: "Turn non-tail recursion into CPS, build trampolines, and know when effects replace CPS."
sources: ["https://dev.realworldocaml.org/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CPS

```ocaml
let rec fact_k n k = if n = 0 then k 1 else fact_k (n - 1) (fun r -> k (n * r))
let fact n = fact_k n Fun.id
let rec map_k f l k = match l with [] -> k [] | x :: t -> map_k f t (fun r -> k (f x :: r))
```

## Notes
- Every call is a tail call, so the stack stays flat; the continuation closures live on the heap instead (allocation cost).
- Defunctionalise the continuation into a variant + `apply` function for efficiency and inspectable stacks.
- Binding operators (`let*`) over a continuation monad make CPS readable.
- With OCaml 5 effects, direct-style code with handlers often replaces hand-written CPS (generators, async).
- Use CPS mainly for deep recursion over trees where a tail-recursive accumulator is not possible.

## Self-check
- [ ] The CPS version handles depth 10^6 without Stack_overflow.

---
id: computing-software.software-engineering.ocaml.stack-depth-and-tail-calls
name: stack-depth-and-tail-calls
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, stack-overflow-tailcalls, stack-overflow, tail-call, ulimit-stack]
level: advanced
status: docs-checked
description: "Avoid Stack_overflow with tail recursion, accumulators, TRMC and know how OCaml 5 sets the stack limit."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/manual/api/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stack depth and tail calls

```ocaml
let rec sum_to acc n = if n = 0 then acc else sum_to (acc + n) (n - 1)     (* tail call: constant stack *)
let rec map f = function [] -> [] | x :: r -> let y = f x in y :: (map f r) [@tail_mod_cons]
```

## Notes
- A call is a tail call if it is the last action in the function body, outside `try ... with`; calls inside `try` are not tail calls.
- In OCaml 5 the stack size limit is the runtime parameter `l` (`stack_limit`, in words) set through `OCAMLRUNPARAM`; OCaml always uses its own stack rather than the operating system's (runtime manual).
- `Stack_overflow` is raised in native code on some platforms only (see its stdlib.mli entry), so do not rely on catching it.
- Fixes: accumulator + `List.rev`, explicit stack with a list/Queue, `Seq`, TRMC (`[@tail_mod_cons]`), CPS conversion.

## Self-check
- [ ] The function processes 10^7 elements without stack growth.

## Checked
2026-11-02. Confirmed: tail_mod_cons attribute (manual), runtime parameter l (runtime manual), Stack_overflow (stdlib.mli). Removed: ulimit/system-stack, 128M-word default, arity and platform-specific claims.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

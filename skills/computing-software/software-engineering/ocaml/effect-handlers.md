---
id: computing-software.software-engineering.ocaml.effect-handlers
name: effect-handlers
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, effects-handlers, effect-perform, effect-deep-handler, continuation, algebraic-effects]
level: advanced
status: docs-checked
description: "Use Effect.perform and Effect.Deep handlers (try_with, match_with, continue, discontinue); continuations are resumed exactly once."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/manual/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Effects

```ocaml
open Effect
open Effect.Deep
type _ Effect.t += Yield : int -> unit Effect.t
let producer () = for i = 1 to 3 do perform (Yield i) done
let () =
  try_with producer ()
    { effc = fun (type a) (e : a Effect.t) ->
        match e with
        | Yield n -> Some (fun (k : (a, _) continuation) -> Printf.printf "got %d\n" n; continue k ())
        | _ -> None }
```

## Notes
- OCaml 5.0+. The compiler does not statically ensure that performed effects are handled; an unhandled effect raises `Effect.Unhandled`.
- A continuation must be used exactly once: resuming twice raises `Continuation_already_resumed`. Every continuation should eventually be resumed with `continue` or `discontinue k exn`.
- `match_with` takes a handler record with `retc` (value), `exnc` (exceptions) and `effc` (effects); `try_with` takes a record with `effc` only.

## Self-check
- [ ] The example prints got 1, got 2, got 3.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the effects chapter (Effect.Unhandled, Continuation_already_resumed, continue/discontinue discipline) and the Effect and Effect.Deep API pages (perform, try_with, match_with, handler records with retc/exnc/effc).

Removed or corrected: the Eio remark and the unconfirmed backtrace remark.

Method: documentation only; no commands were run.

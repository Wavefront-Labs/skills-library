---
id: computing-software.software-engineering.ocaml.result-based-error-handling
name: result-based-error-handling
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, result-error-style, result-type, error-monad, let-star-result]
level: practitioner
status: docs-checked
description: "Use the Stdlib Result module with typed or polymorphic-variant errors and bind operators for expected failures."
sources: ["https://ocaml.org/manual/5.5/api/Result.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Result-based error handling

```ocaml
let ( let* ) = Result.bind
let ( let+ ) r f = Result.map f r
let parse_port s =
  match int_of_string_opt s with
  | None -> Error (`Bad_int s)
  | Some p when p < 1 || p > 65535 -> Error (`Out_of_range p)
  | Some p -> Ok p
let config host port =
  let* port = parse_port port in
  let+ host = if host = "" then Error `Empty_host else Ok host in
  (host, port)
```

## Notes
- `Result` (since OCaml 4.08) handles computation results and errors explicitly without exceptions. `('a, 'e) Result.t` is `Ok of 'a | Error of 'e`.
- Core functions: `ok`, `error`, `value r ~default`, `bind r f` (short-circuits on `Error`), `map f r`, `map_error f r`, `join`, `fold ~ok ~error r`, `iter`, `iter_error`, `is_ok`, `is_error`, `to_option`, `to_list`, `to_seq`, `equal`, `compare`. `Result.Syntax` also exists.
- Newer in 5.4: `product r0 r1` (pair, returning the first error), `error_to_failure`, `get_ok'` and `retract`.
- `get_ok r` and `get_error r` raise `Invalid_argument` on the wrong constructor, so treat them as assertions.
- Error types can be polymorphic variants (as above) so different functions' errors compose under `let*`.

## Self-check
- [ ] The `let*` chain compiles and each step's error type unifies.

## Checked
Date: 2026-11-08. Confirmed against the OCaml 5.5 Stdlib `Result` API page (value list read in full; the `Result.Syntax` submodule page was not read). Removed: the exceptions-versus-results policy, `Format.kasprintf` and `try_` helper advice, the Jane Street `Or_error` comparison and the Real World OCaml source (not read).
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.ocaml.option-result-and-either
name: option-result-and-either
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, option-result-either, option-module, result-module, either-module]
level: practitioner
status: docs-checked
description: "Use Option, Result and Either combinators (map, bind, value, to_option), and convert between error styles."
sources: ["https://ocaml.org/manual/api/", "https://ocaml.org/docs", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Option, Result, Either

```ocaml
Option.map (( + ) 1) (Some 1)           Option.value ~default:0 None
Option.bind (Some 2) (fun x -> if x > 1 then Some x else None)
Result.map succ (Ok 1)    Result.bind r f    Result.map_error f r
Result.to_option r        Result.get_ok r   (* raises Invalid_argument on Error *)
List.partition_map (function `A x -> Either.Left x | `B y -> Either.Right y) l
```

## Notes
- `('a, 'e) result = Ok of 'a | Error of 'e`; `Result.join`, `Result.fold ~ok ~error`, `Result.iter`.
- `Option.is_some/is_none/get/to_list/to_result ~none`.
- `Either.t = Left | Right` (4.12+), distinct from result: neither side is an error.

## Self-check
- [ ] No `Option.get` / `Result.get_ok` on values that can be absent.

## Checked
2026-11-02. Confirmed: Option/Result/Either function signatures and raising behaviour (option.mli, result.mli, either.mli), Either since 4.12. Removed: Fun.protect remark.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

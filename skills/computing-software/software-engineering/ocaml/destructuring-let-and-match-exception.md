---
id: computing-software.software-engineering.ocaml.destructuring-let-and-match-exception
name: destructuring-let-and-match-exception
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, let-patterns-exception, match-exception, destructuring-let, irrefutable-pattern]
level: practitioner
status: docs-checked
description: "Destructure tuples/records in let and function arguments, and use match ... with exception to separate success cases from raised errors."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Destructuring and `match ... with exception`

```ocaml
let (q, r) = (7 / 2, 7 mod 2)
let area { w; h } = w * h               (* record pattern in args *)
let first_line ic =
  match input_line ic with
  | line -> Some line
  | exception End_of_file -> None
```

## Notes
- `let Some x = o in ...` triggers warning 8 (non-exhaustive) and raises `Match_failure` when the match fails.
- `match e with exception X -> ... | v -> ...` keeps the success arms outside the handler: only the matched expression `e` is covered by the exception cases (manual, exception patterns).
- `fun (a, b) -> ...` takes a pattern; labelled args accept patterns: `let f ~x:(a, b) = ...`.

## Self-check
- [ ] Success arms of a `match ... with exception` are not wrapped by the handler.

## Checked
2026-11-02. Confirmed: match ... with exception semantics and Match_failure (manual expr/patterns), `~label:pattern` argument syntax (manual expr). Removed: the claim that only tuples and single-constructor records are irrefutable, and a restatement of try.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

---
id: computing-software.software-engineering.ocaml.pattern-forms-guards-and-or
name: pattern-forms-guards-and-or
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, patterns-guards, ocaml-patterns, or-pattern, when-guard, as-pattern, char-range]
level: practitioner
status: docs-checked
description: "Combine or-patterns, as-aliases, when-guards, char ranges and nested patterns; avoid unused-case and fragile-match warnings."
sources: ["https://ocaml.org/manual/", "https://ocaml.org/docs", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pattern forms

```ocaml
let classify = function
  | 0 | 1 -> "small"
  | n when n < 0 -> "negative"
  | _ -> "big"
let kind = function 'a'..'z' -> `Lower | 'A'..'Z' -> `Upper | _ -> `Other
let f = function (Some _ as o) -> o | None -> None   (* 'as' names the whole value *)
let rec dedup = function
  | a :: (b :: _ as rest) when a = b -> dedup rest
  | x :: r -> x :: dedup r
  | [] -> []
```

## Notes
- Or-patterns must bind the same variables with the same types: `A x | B x`.
- Warnings: 8 non-exhaustive, 11/12 redundant case/subpattern, 4 fragile match (off by default; enable with `-w +4` for variants you control).
- Lists `[a; b]`, `a :: rest`, arrays `[| a; b |]`, records `{ f = p; _ }` all work in patterns.

## Self-check
- [ ] Build output has no warning 8 for the match.

## Checked
2026-11-02. Confirmed: pattern grammar: char ranges, `as`, or-patterns, array/record/list patterns (manual patterns); warning numbers 4/8/11/12 (warnings.ml). Removed: guard-exhaustiveness and literal remarks.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

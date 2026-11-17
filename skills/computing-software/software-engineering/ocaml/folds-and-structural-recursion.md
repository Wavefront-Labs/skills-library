---
id: computing-software.software-engineering.ocaml.folds-and-structural-recursion
name: folds-and-structural-recursion
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, folds-recursion, ocaml-functional-idioms, fold-left, fold-right, accumulator, structural-recursion]
level: intro
status: docs-checked
description: "Choose fold_left vs fold_right, write structural recursion with accumulators, and replace loops with folds safely."
sources: ["https://dev.realworldocaml.org/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Folds and recursion

```ocaml
let sum l = List.fold_left ( + ) 0 l
let rev l = List.fold_left (fun acc x -> x :: acc) [] l
let map f l = List.rev (List.fold_left (fun acc x -> f x :: acc) [] l)
let rec length_acc acc = function [] -> acc | _ :: t -> length_acc (acc + 1) t
let max_by f = function [] -> None | x :: xs -> Some (List.fold_left (fun m y -> if f y > f m then y else m) x xs)
```

## Notes
- `fold_left f init l` goes left to right; the List docs flag `List.fold_right` as not tail-recursive, so it uses stack proportional to the list length.
- Signature: `fold_left : ('acc -> 'a -> 'acc) -> 'acc -> 'a list -> 'acc`.
- Recursion follows the data type: one case per constructor. Add an accumulator for tail recursion.
- `List.iter` for effects, `List.map` for transforms, `fold` for aggregates, `List.exists/for_all/find_opt` for searches (short-circuit).
- Do not use `@` in a loop to append single elements (quadratic).

## Self-check
- [ ] `rev [1;2;3] = [3;2;1]` and a 10^6-element list does not overflow.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the List API page (fold_left and fold_right signatures, fold_right not tail-recursive, exists, for_all, find_opt).

Removed or corrected: the vague 'until recent versions' remark on fold_right.

Method: documentation only; no commands were run.

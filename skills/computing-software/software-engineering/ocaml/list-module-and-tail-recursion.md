---
id: computing-software.software-engineering.ocaml.list-module-and-tail-recursion
name: list-module-and-tail-recursion
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, list-module, ocaml-stdlib-collections, list-map, tail-recursion, list-fold, tail-mod-cons]
level: practitioner
status: docs-checked
description: "Use the List module, understand stack use of non-tail-recursive functions, and choose rev/append patterns and TRMC safely."
sources: ["https://ocaml.org/manual/api/", "https://ocaml.org/docs", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# List and tail recursion

```ocaml
List.map succ [1;2;3]     List.filter_map f l     List.fold_left ( + ) 0 l
List.assoc_opt "k" [("k", 1)]   List.sort compare l   List.init 3 Fun.id
List.rev_append (List.rev xs) ys   (* tail-recursive append *)
```

## Notes
- Some List functions are not tail-recursive and use stack space proportional to the list length (list.mli lists which). For huge lists use `List.rev_map`+`List.rev`, `rev_append`, or fold + reverse.
- Mark your own functions `[@tail_mod_cons]` to get tail-modulo-cons; the compiler reports an error if it cannot apply the transformation (manual).
- `List.nth` raises `Failure` (list too short) or `Invalid_argument` (negative index); use `List.nth_opt`.
- `List.stable_sort` is stable (merge sort); `List.sort` is the same or faster but not guaranteed stable. `List.sort_uniq` removes duplicates.
- `List.mem`, `List.assoc` use structural equality; use `List.exists`/`List.find_opt` with typed equality.

## Self-check
- [ ] A 1,000,000-element `List.map`/your recursive function does not raise `Stack_overflow` on your target OCaml version.

## Checked
2026-11-02. Confirmed: tail-recursion note, nth exceptions, sort/stable_sort (list.mli), tail_mod_cons attribute and its error (manual tail-mod-cons). Removed: the per-function pre-5.1 history and 100k figure, O(n) remark, sort-is-stable claim (fixed).
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.

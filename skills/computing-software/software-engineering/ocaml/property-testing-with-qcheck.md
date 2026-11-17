---
id: computing-software.software-engineering.ocaml.property-testing-with-qcheck
name: property-testing-with-qcheck
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, qcheck, property-based-testing, shrinking, generators]
level: advanced
status: docs-checked
description: "Write generators, properties and shrinkers with QCheck (or qcheck-alcotest) and find minimal counterexamples."
sources: ["https://github.com/c-cube/qcheck"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# QCheck

```lisp
(test (name props) (libraries qcheck-core qcheck-alcotest mylib))
```
```ocaml
let prop_rev = QCheck.Test.make ~count:1000 ~name:"rev involutive"
  QCheck.(list int) (fun l -> List.rev (List.rev l) = l)
let () = Alcotest.run "props" [ "qcheck", List.map QCheck_alcotest.to_alcotest [prop_rev] ]
```

## Notes
- Packages: `qcheck-core` (depends only on unix and dune), `qcheck-ounit`, `qcheck-alcotest`, `qcheck` (compatibility API), `ppx_deriving_qcheck` (derives generators from types). `qcheck-stm`, `qcheck-lin` and `qcheck-multicoretests-util` come from the separate multicoretests repository, not this one.
- Tests are built with `QCheck.Test.make ~count ~name arbitrary property`; run standalone with `QCheck.Test.check_exn`, or via `QCheck_base_runner.run_tests` / `run_tests_main`.
- Built-in generators come with printers and shrinkers. Custom arbitraries use `QCheck.make ~print ~shrink`; `QCheck.Shrink` and `QCheck.Iter` help build shrinkers. `QCheck2` has integrated shrinking but is less battle-tested.
- Combinators include `fix`, `sized`, `oneof_weighted`, `map`, `map2`; `QCheck.assume` handles preconditions; `~long_factor` multiplies the count for a long run.
- Runs print the random seed, which changes each run. The README does not document an environment variable for replay; check the runner's options in the API docs.
- Properties to try: round trips, idempotence, comparison against a simple reference model.

## Self-check
- [ ] A deliberately broken function is caught with a small shrunk example (the README shows `[0; 1]` for a wrong `List.rev` property).

## Checked
Checked 2026-11-08 against the QCheck README (the old source was the Alcotest repo). Removed: the `QCHECK_SEED` replay claim (not in the README), the generator examples `list_of_size`, `pair`, `option` (not shown there), and qcheck-stm as part of this repo. Corrected the package list. Unchanged: the example code, adapted from the README's `List.rev` example and not compiled here.

Method: documentation only; no commands were run.

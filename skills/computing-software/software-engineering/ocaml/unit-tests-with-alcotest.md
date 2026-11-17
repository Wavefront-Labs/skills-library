---
id: computing-software.software-engineering.ocaml.unit-tests-with-alcotest
name: unit-tests-with-alcotest
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, alcotest, ocaml-testing, unit-testing, testable, test-case]
level: practitioner
status: docs-checked
description: "Write Alcotest suites with test_case, check functions and custom testables, run them via dune test, and filter by name, speed or tag."
sources: ["https://github.com/mirage/alcotest", "https://dune.readthedocs.io/en/stable/tests.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alcotest

```lisp
; test/dune
(test (name test_main) (libraries alcotest mylib))
```
```ocaml
let test_add () = Alcotest.(check int) "same" 3 (Mylib.add 1 2)
let test_list () = Alcotest.(check (list string)) "order" ["a";"b"] (Mylib.names ())
let user = Alcotest.testable (fun ppf u -> Fmt.pf ppf "%s" u.name) ( = )
let () = Alcotest.run "mylib" [ "math", [ Alcotest.test_case "add" `Quick test_add ] ]
```

## Notes
- Run with `dune test` (runs every test under the current directory). The executable itself takes a `test` subcommand that filters by regular expression on test names, optionally with test numbers or ranges (e.g. `2,4..9`), and `list` shows the tests.
- `Quick tests run on every invocation; `Slow tests are for occasional stress runs and `-q` skips them.
- `Alcotest.run` takes a name and a list of suites; `Alcotest.group` nests tests under dotted names.
- `check` takes a testable, a message, then expected and actual. A testable bundles a pretty-printer and a comparator (`Alcotest.testable pp equal`).
- By default only the first failing test's log is printed; `--show-errors` prints all. Full results are in `_build/_tests`.
- `--tags` / `ALCOTEST_TAGS` select tags; `run_with_args` passes a Cmdliner-parsed option to every test.
- `Alcotest_lwt` wraps `unit -> unit Lwt.t` tests and calls `Lwt_main.run` for you. The repo also contains an alcotest-async package; its usage is not described in the README.

## Self-check
- [ ] A deliberately wrong expectation fails with a readable diff.

## Checked
Checked 2026-11-08 against the Alcotest README and dune's tests page. Removed: the `test math 0` command example (README says filtering is a regex on names and number ranges), `check_raises`/`fail`/`failf` (not in the README), and the "expected first" argument-order claim beyond what the example shows. Unchanged: dune stanza and the code example, which were not compiled.

Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.ocaml.unit-tests-with-ounit2
name: unit-tests-with-ounit2
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, ounit2, assert-equal, test-fixtures]
level: practitioner
status: draft
description: "Write OUnit2 suites with >:: and assert_equal ~printer, bracket fixtures, and run via dune test or the test runner flags."
sources: ["https://github.com/mirage/alcotest", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OUnit2

```lisp
(test (name tests) (libraries ounit2 mylib))
```
```ocaml
open OUnit2
let t_add _ = assert_equal ~printer:string_of_int 3 (Mylib.add 1 2)
let suite = "mylib" >::: [ "add" >:: t_add;
  "raises" >:: (fun _ -> assert_raises Not_found (fun () -> Mylib.find "x")) ]
let () = run_test_tt_main suite
```

## Notes
- The test function receives a `test_ctxt`; use `bracket setup teardown ctxt` for fixtures that clean up.
- `~printer` makes failure messages readable; default error prints no values.
- Runner flags: `-only-test mylib:0:add`, `-list-test`, `-runner sequential`, `-shards N`.
- Package name `ounit2` (the old `oUnit` is OUnit 1).
- Compare with Alcotest: OUnit has fixtures and parallel shards; Alcotest has nicer output.

## Self-check
- [ ] `dune test` prints failures with expected/actual values.

---
id: computing-software.software-engineering.ocaml.expect-tests-with-ppx-expect
name: expect-tests-with-ppx-expect
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, ppx-expect, expect-test, inline-tests, dune-promote]
level: practitioner
status: docs-checked
description: "Write let%expect_test blocks that print output, accept corrections with dune promote, and sanitise non-deterministic output."
sources: ["https://github.com/janestreet/ppx_expect", "https://dune.readthedocs.io/en/stable/tests.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ppx_expect

```lisp
(library (name mylib) (inline_tests) (preprocess (pps ppx_expect ppx_inline_test)))
```
```ocaml
let%expect_test "greet" =
  print_endline (greet "ann");
  [%expect {| Hello, ann |}]
let%test "sum" = sum [1;2;3] = 6
```

## Notes
- ppx_expect is described as a framework for tests "similar to Cram", built on inline tests. A failing test produces a `.corrected` file and a diff. Dune's tests page says `dune promote` accepts the correction, and `dune runtest --auto-promote` accepts it right after the run.
- The ppx_expect README gives no dune stanza: it says to follow the same rules as ppx_inline_test. The stanza above is the common form and should be checked against the ppx_inline_test README.
- Each `[%expect]` block matches the output since the previous block; matching normalises whitespace, so indentation differences can still pass. `-expect-test-strict-indentation=true` makes the runner correct badly formatted blocks.
- `[%expect.unreachable]` marks code that should not be reached; if reached, the correction becomes an `[%expect]` with the output so far. An `[%expect]` never reached becomes `[%expect.unreachable]`.
- `[%expect_exact]` keeps the exact output including leading and trailing newlines and indentation.
- Non-deterministic output: capture it with `[%expect.output]` and post-process (e.g. replace digits in timestamps), or set the `sanitize` hook in `Expect_test_config`.
- Uncaught exceptions appear in `[@@expect.uncaught_exn]`, which keeps stack traces; the README's exception example calls `Printexc.record_backtrace false`.

## Self-check
- [ ] Changing the implementation produces a diff that `dune promote` can accept.

## Checked
Checked 2026-11-08 against the ppx_expect README and dune's tests page (the old source was the Alcotest repo). Removed: "from Jane Street" and "function level versus cram" framing beyond the README's Cram comparison, the `inline_test_runner` and executables remark, and the claim that `let%test` comes from the same README. Unchanged: the example code and stanza, flagged above as not verified from the README.

Method: documentation only; no commands were run.

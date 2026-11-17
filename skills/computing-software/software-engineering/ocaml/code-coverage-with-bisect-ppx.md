---
id: computing-software.software-engineering.ocaml.code-coverage-with-bisect-ppx
name: code-coverage-with-bisect-ppx
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, coverage-bisect, bisect-ppx, code-coverage, instrument-with]
level: practitioner
status: docs-checked
description: "Instrument with bisect_ppx via dune --instrument-with, run tests and produce HTML, summary or Coveralls reports."
sources: ["https://github.com/aantron/bisect_ppx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bisect_ppx coverage

```lisp
(library (name mylib) (instrumentation (backend bisect_ppx)))
```
```bash
dune runtest --instrument-with bisect_ppx --force
bisect-ppx-report html           # output in _coverage/index.html
bisect-ppx-report summary
bisect-ppx-report send-to Coveralls   # in the CI script
```

## Notes
- Add `"bisect_ppx" {dev & >= "2.5.0"}` to the opam `depends` (README).
- `--instrument-with bisect_ppx` instruments the code under test; plain `dune runtest` is uninstrumented. `--force` forces all tests to run, which the README says is needed for an accurate report.
- `.coverage` files (e.g. `bisect0123456789.coverage`) are written when the test binary exits; the README gives no fixed directory, so clean them with `find . -name '*.coverage'` between runs.
- `send-to Codecov` is also supported. On GitHub Actions to Coveralls the README sets `COVERALLS_REPO_TOKEN` to `${{ secrets.GITHUB_TOKEN }}` and `PULL_REQUEST_NUMBER` to `${{ github.event.number }}`.
- Exclusions: `[@coverage off]` on an expression, `[@@coverage off]` on a top-level `let`, `[@@@coverage off]` / `[@@@coverage on]` around a block, `[@@@coverage exclude_file]` for a whole file.

## Self-check
- [ ] HTML report highlights uncovered code.

## Checked
Checked 2026-11-08 against the bisect_ppx README (the previous source was the Alcotest repo, which does not cover this). Removed: the `opam install bisect_ppx` line, the "CWD of the test run" claim and `dune test` wording (README uses `dune runtest`), and the "uncovered branches" phrasing. Unchanged: the instrumentation stanza, `--force`, report subcommands.

Method: documentation only; no commands were run.

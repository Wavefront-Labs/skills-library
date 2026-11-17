---
id: computing-software.software-engineering.ocaml.dune-custom-rules-and-cram-tests
name: dune-custom-rules-and-cram-tests
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, dune-rules-cram, dune-rule, cram-tests, dune-actions, dune-deps]
level: advanced
status: docs-checked
description: "Generate files with (rule), declare (deps) and (action), and write cram tests (.t files) for CLI behaviour."
sources: ["https://dune.readthedocs.io/", "https://github.com/ocaml/dune/blob/main/doc/reference/dune/rule.rst", "https://github.com/ocaml/dune/blob/main/doc/reference/cram.rst", "https://github.com/ocaml/dune/blob/main/doc/reference/dune/cram.rst", "https://github.com/ocaml/dune/blob/main/doc/reference/dune-project/cram.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dune rules and cram tests

```lisp
(rule
 (targets version.ml)
 (deps (:gen gen.exe))
 (action (with-stdout-to version.ml (run %{gen}))))
(rule (alias runtest) (action (diff expected.txt actual.txt)))
```
```
# test/cli.t  (a file named *.t)
  $ hello --name Ann
  Hello, Ann
```
```lisp
(cram (deps %{bin:hello}))
```

## Notes
- A rule needs at least one target or at least one alias. Targets must be statically known and may be inferred from the action; user rules have no `%.y` from `%.x` patterns.
- By default a rule's target must not already exist in the source tree. `(mode promote)` copies targets back to the source tree after running (useful when generated code is easier to review than the generator); `fallback` ignores the rule when targets exist in the source tree.
- `(diff <file1> <file2>)` is like `diff` but allows promotion (`dune promote`). `(with-stdout-to <file> <action>)` redirects stdout.
- Variables used here: `%{dep:path}` declares a dependency; `%{bin:<program>}` resolves a binary; `(glob_files <glob>)` and `(source_tree <dir>)` are dependency forms; `(:name deps)` binds a list of dependencies to a name.
- Cram tests are shell sessions: a line starting with two spaces then `$ ` is a command, `>` continuation lines (two spaces, `> `) continue it, other indented lines are the expected output (a nonzero exit code appears as `[1]`), and unindented lines are comments.
- File tests are files with a `.t` extension; directory tests are `run.t` inside a directory whose name ends in `.t`. A test runs in a temporary directory containing only the dependencies from `cram` stanzas (plus the directory's contents for directory tests).
- `dune runtest` runs all cram tests. The run produces a corrected file offered for promotion; apply with `dune promote`.
- A `cram` stanza configures tests: `(deps ...)` (default none; depend on the binary under test so Dune re-runs the test and makes it visible), `(applies_to ...)`, `(enabled_if ...)`, `(alias ...)`, `(timeout <float>)` (since 3.20), `(shell <sh|bash>)` (since 3.22; default `sh`).
- Cram tests are enabled by default from dune language 3.0; `(cram enable)` or `(cram disable)` in `dune-project` sets it.
- A command that exits the shell early marks later commands `***** UNREACHABLE *****`; for example `source foo.sh` without `./` can exit the POSIX `sh`.

## Self-check
- [ ] A clean `dune clean && dune runtest` succeeds, proving dependencies are declared.

## Checked
Date: 2026-11-08. Confirmed against Dune docs source on GitHub: reference/dune/rule.rst, reference/cram.rst, reference/dune/cram.rst, reference/dune-project/cram.rst, reference/actions/diff.rst and with-outputs-to.rst, concepts/variables.rst and dependency-spec.rst. Removed: the `%{read:file}` and `%{ocaml_version}` details, and the claim about rules running in sandboxes under `_build/default/<dir>` (not stated on the pages read).
Method: documentation only; no commands were run.

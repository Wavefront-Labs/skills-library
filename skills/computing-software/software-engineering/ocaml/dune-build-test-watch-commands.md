---
id: computing-software.software-engineering.ocaml.dune-build-test-watch-commands
name: dune-build-test-watch-commands
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, dune-commands, dune-watch, dune-promote, dune-runtest, dune-alias]
level: practitioner
status: docs-checked
description: "Use dune build/test/exec/promote, watch mode (-w), targets and @aliases, and profile selection with --profile."
sources: ["https://dune.readthedocs.io/en/stable/usage.html", "https://dune.readthedocs.io/en/stable/quick-start.html", "https://dune.readthedocs.io/en/stable/tests.html", "https://dune.readthedocs.io/en/stable/reference/aliases.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dune commands

```bash
dune build                  # no targets given: builds the default alias
dune build @check           # a target starting with @ is an alias
dune test                   # same as dune runtest / dune build @runtest
dune exec -- ./hello_world.exe   # build and run in one step
dune build -w               # watch mode (also dune test -w)
dune promote                # accept corrected expect-test output
dune runtest --auto-promote # accept corrections right after the run
dune build --profile foo    # select a build profile
dune build @fmt --auto-promote   # formatting, see ocamlformat skill
```

## Notes
- Artifacts go in `_build` (relative to the workspace); `--build-dir` changes it.
- `dune test` (or `dune runtest`) runs the tests in the current directory and children recursively; `dune test foo/bar` targets a subdirectory.
- Watch mode (`-w`/`--watch`) is supported by `dune build` and `dune runtest`; it needs `inotifywait` or `fswatch` installed.
- `-j N` sets parallel jobs (default: detected CPU cores); `DUNE_JOBS` also sets it, command line wins. `--root` disables the automatic root lookup, and targets are then relative to that root.
- Built-in aliases listed in the reference include `@all`, `@default`, `@install`, `@check`, `@runtest`, `@fmt`, `@doc`.
- Merlin gets its configuration from dune; since dune 2.8 `.merlin` files are not promoted into source directories.
- If the build says a library is not found, check `(libraries ...)` and install it with opam.

## Self-check
- [ ] `dune test` shows no diffs; any expected output change is promoted deliberately.

## Checked
Checked 2026-11-08 against the dune usage, quick-start, tests and aliases pages. Removed: the claim that dev profile makes warnings errors and release optimises (those pages do not state it), `dune clean`, `dune rules`/`dune describe`, `--release`, and the `| head` tip; the alias list was cut to those the reference shows. Unchanged: exec, test, promote, watch, -j and --root behaviour.

Method: documentation only; no commands were run.

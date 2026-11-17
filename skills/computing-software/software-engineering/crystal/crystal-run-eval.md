---
id: computing-software.software-engineering.crystal.crystal-run-eval
name: crystal-run-eval
category: computing-software
field: software-engineering
product: crystal
tags: [crystal-run-eval, cli-build-run, crystal-run, crystal-eval, script, stdin, one-liner, program-args, crystal]
level: intro
status: docs-checked
description: "Run Crystal source directly with crystal run, pass program arguments after --, evaluate code with crystal eval from an argument or stdin."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/man/crystal/README.md
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/command.cr
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/command/eval.cr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crystal run and crystal eval

Goal: use Crystal like a script runner.

- `crystal [run] [<options>] <programfile> [-- <argument>...]` compiles to a temporary location and runs immediately. Arguments after `--` go to the program, for example `crystal run hello_world.cr -- Crystal` makes `ARGV[0]` equal `"Crystal"`.
- `crystal run` is the default command, and a bare file name also works: `crystal app.cr arg1` runs the file with `arg1` as an argument.
- The program's stdin, stdout and stderr are inherited, and its exit code becomes the compiler's exit code.
- `crystal eval [<options>] [<source>]` compiles and runs source from the command line, or from standard input if no source is given: `crystal eval 'puts "Hello World"'` or `echo 'puts "Hello World"' | crystal eval`.
- Common options for both: `-O LEVEL`, `--release` (equivalent to `-O3 --single-module`), `--no-debug`, `--progress`, `--static`, and `-D FLAG` to define a compile-time flag. `eval` also takes `-o <output_file>`.

Gotchas:
- Each run compiles first; for repeated use build once with `crystal build`.
- Put program arguments after `--` so they are not parsed as compiler options.
- Interactively, close stdin with `Ctrl+D`.

Verify: `crystal run app.cr -- a b` shows `ARGV` as `["a", "b"]`.

## Checked

2026-11-03. Confirmed against the Crystal compiler manual (`run`, `eval` synopses, options, stdin note) and the command source (bare-file form, argument handling, inherited stdio, exit-code propagation, `-D` option).
Removed: the shebang and caching claim, `crystal eval` having no file context for `require "./x"`, and the sample `exit 3` / uncaught-exception exit codes.
Method: documentation only; no commands were run.

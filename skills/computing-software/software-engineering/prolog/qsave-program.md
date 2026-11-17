---
id: computing-software.software-engineering.prolog.qsave-program
name: qsave-program
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, qsave-program, saved-state]
level: advanced
status: docs-checked
description: "Build a standalone SWI-Prolog saved state with swipl -o -c or qsave_program/2 and run it with its options and limits."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/man/runtime.plx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Saved states
```prolog
:- initialization(main, main).
main :- writeln(hello).
```
```bash
swipl -o app -c app.pl                 # load app.pl and save a state as ./app
./app
swipl -x app arg1 arg2                 # run a saved state through -x
```
- `-c` loads the files and calls `qsave_program/2` with options built from the command line; `qsave_program(File)` is `qsave_program(File, [])`.
- Options of `qsave_program(File, Options)`: `goal(Callable)` (initialization goal, like `-g`; `prolog` starts the toplevel, `default` halts if there are initialization goals), `toplevel(Callable)` (like `-t`), `stack_limit(Bytes)`, `init_file(Atom)`, `class(runtime|development)`, `autoload(Bool)` (default true), `map(File)`, `op(save|standard)`, `stand_alone(Bool)`, `emulator(File)`.
- `stand_alone(true)` puts the emulator at the start of the state so the result is a single executable, independent of the build location provided all libraries are loaded.
## Gotchas
- Directives that do more than set predicate attributes or load files must be `initialization/1,2` goals if they have to run when the state starts; `initialization(go, main)` starts an application.
- Blobs such as streams, threads and clause references cannot be saved.
- 32-bit compiled code does not run on a 64-bit emulator, nor the other way around.
- Foreign libraries need the foreign-context handling described in the manual (`--foreign=save|copy`).
## Self-check
Build `app`, run `./app`, and check the exit status.

## Checked

2026-11-03. SWI-Prolog manual chapter "Deploying applications" (runtime.plx in swipl-devel/man): `swipl -o state -c file.pl`, `swipl -x state`, qsave_program/1,2 option list and meanings, limitations list, 32/64-bit footnote, `--foreign=save|copy` examples. Removed: the Docker image line, the `-g "qsave_program(...)"` one-liner and the "version-specific" claim (replaced by the documented 32/64-bit footnote).

Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.nim.nimble-tasks-and-commands
name: nimble-tasks-and-commands
category: computing-software
field: software-engineering
product: nim
tags: [nimble-tasks-and-commands, nimble-package-file, nimble-build, nimble-run, nimble-test, nimble-task, nimble-develop, task, setup, nim]
level: practitioner
status: docs-checked
description: "Use nimble build, run, test, install, check, tasks, develop and setup, define custom tasks with before/after hooks, and forward compiler flags."
sources:
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/create-packages.md
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/workflow.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nimble tasks, build, run and test

Goal: standardise project commands.

- `nimble build` builds the package with default flags: a debug build with stack traces. `nimble install` builds in release mode instead. Nim flags given to `nimble build` (or `install`) are forwarded to the compiler; make them persistent in Nim config files.
- `nimble run` builds and runs a binary from the `bin` list. With several binaries, name the binary after any compilation flags; flags after the binary or `--` go to the binary. `--package, -p` runs a binary from a dependency: `nimble --package:foo run <compilation_flags> bar <run_flags>`.
- `nimble test` is a predefined task that compiles and runs every file in `tests` whose name begins with `t`; Nim flags are forwarded. Override it with `task test, "General tests":` and `exec "nim r --hints:off tests/" & file`.
- `nimble c` (also `compile`, `js`, `cc`, `cpp`) compiles individual modules; with `c`/`compile` Nimble uses the `backend` set in the .nimble file.
- Custom tasks live in the .nimble file: `task hello, "This is a hello task":` runs with `nimble hello`; `nimble tasks` lists them. Tasks may use any Nim code that does not touch the FFI, plus the nimscript module (for example external processes).
- Hooks: `before hello:` and `after hello:` blocks run around any Nimble command, including your tasks; returning `false` from them stops further execution.
- Flag order for tasks: `nimble <compflags> task <runflags>`. Compile flags go to the compiler running the .nimble file; run flags are read through `commandLineParams`. To pass compiler flags to an `exec("nim ...")` inside a task, take them from the run flags and forward them yourself.
- `nimble develop` puts packages in develop mode (adds paths to `nimble.develop`); `nimble setup` writes `nimble.paths` and hooks it into `config.nims`.

Gotchas:
- `nimble.develop` and `nimble.paths` are user specific and must not be committed.

Verify: `nimble tasks` lists your task and `nimble test` passes.

## Checked

2026-11-03. Confirmed in the Nimble guide pages "Creating Nimble packages" (build, install, run, test, c, tasks, hooks, flag order) and "Develop workflow" (develop, setup, files not to commit). Removed: `nimble install -y` and `nimble docs` examples, the "tasks run in the package root" and "test stops at the first compile failure" gotchas, and the `-d:release --mm:orc` example flags.
Method: documentation only; no commands were run.

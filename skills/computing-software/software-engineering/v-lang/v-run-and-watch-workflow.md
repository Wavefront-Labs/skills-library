---
id: computing-software.software-engineering.v-lang.v-run-and-watch-workflow
name: v-run-and-watch-workflow
category: computing-software
field: software-engineering
product: v-lang
tags: [v-run-and-watch-workflow, v-cli-run-and-build, v run, v watch, v repl, repl, script, run args, live reload, v-lang]
level: intro
status: draft
description: "Iterate fast with v run, v watch run, scripts with args and the v repl, plus useful shell integration."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# v run, v watch and the REPL

Goal: tight edit-run loops.

- `v run file.v arg1 arg2` or `v run .` for a module directory; arguments are available through `os.args` (index 0 is the program path).
- `v watch run .` recompiles and restarts on file changes (confirm availability in your version).
- `v -live run app.v` with `@[live]` functions reloads code in-process (experimental).
- `v repl` starts an interactive session; statements persist and `println` is automatic for expressions.
- Scripts: first-line `#!/usr/bin/env -S v run` plus `chmod +x` lets you run `./script.vsh`; `.vsh` files allow top-level statements and `os` imported by default.
- `v -cg` is a shortcut for debug C output; `v -v` prints verbose compiler stages.

Gotchas:
- REPL cannot define structs over multiple lines easily; use a file for larger code.
- `v run` creates temp binaries under the system temp dir; clean them with `v wipe-cache`.

Verify: `v run hello.v a b` prints args.

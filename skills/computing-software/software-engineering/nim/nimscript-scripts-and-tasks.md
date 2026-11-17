---
id: computing-software.software-engineering.nim.nimscript-scripts-and-tasks
name: nimscript-scripts-and-tasks
category: computing-software
field: software-engineering
product: nim
tags: [nimscript-scripts-and-tasks, nimscript, nims, nim-e, task, exec, mkdir, cpfile, rmfile, build-script, nim]
level: practitioner
status: docs-checked
description: "Write NimScript build scripts with nim e, define named tasks and use exec, cd, mkDir, cpFile and friends."
sources:
  - https://nim-lang.org/docs/nims.html
  - https://nim-lang.org/docs/nimscript.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running .nims scripts and defining tasks

Goal: replace shell/Make build scripts with portable Nim.

- Run a script: `nim myscript.nims` (or `nim e`, "run a Nimscript file"). On Unix the shebang `#!/usr/bin/env nim` works when the file ends in `.nims`; `#!/usr/bin/env -S nim e --hints:off` disables hints and relaxes the extension constraint.
- Tasks: the `task` template turns a script into a build tool, for example `task build, "builds an example": setCommand "c"`. By convention the tasks are `help` (list tasks with docstrings), `build`, `tests`, `bench`. Nimble integration is described in the Nimble readme.
- APIs from the `nimscript` module: `exec`, `cd`, `withDir`, `mkDir`, `rmDir`, `rmFile`, `cpFile`, `cpDir`, `mvFile`, `listFiles`, `listDirs`, `fileExists`, `dirExists`, `getEnv`, `putEnv`, `selfExec`, `thisDir`, and `mode = ScriptMode.Verbose|Silent`.
- Config files: `switch("opt", "size")` equals `--opt:size`; the `--opt:size` template form also works. Config scripts are read from the user config dir, parent dirs, `config.nims` in the project dir and `$project.nims`.
- Many stdlib modules work in the VM, among them algorithm, json, math, os, strutils, strformat (see the Standard library modules list in the nims guide; `tables` and `sequtils` are not in it).

Gotchas:
- Nim's FFI is not available in NimScript, so any stdlib module that relies on `importc` cannot be used; multimethods and `ref ref int` are unsupported.

Verify: running the script performs the task steps.

## Checked

2026-11-02. Confirmed against nims.md (running, shebang, tasks, limitations, module list, `switch`) and lib/system/nimscript.nim (exported procs). Removed: `before`/`after` hooks, `gorge`/`quit` as nimscript APIs, `sequtils`/`tables`/threads/async statements, the `nim build` invocation.
Method: documentation only; no commands were run.

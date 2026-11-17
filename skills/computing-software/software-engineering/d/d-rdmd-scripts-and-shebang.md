---
id: computing-software.software-engineering.d.d-rdmd-scripts-and-shebang
name: d-rdmd-scripts-and-shebang
category: computing-software
field: software-engineering
product: d
tags: [d-rdmd-scripts-and-shebang, dev-tools, rdmd, d-script, shebang, eval, loop, scripting, dmd-wrapper, --eval, d]
level: intro
status: docs-checked
description: "Run D source directly with rdmd (auto dependency discovery, caching), shebang scripts, --eval one-liners, --loop, -run options and passing flags to dmd."
sources:
  - https://dlang.org/rdmd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rdmd: running D files as scripts, --eval, --loop and shebang

Goal: use D for scripts and quick experiments.

- `rdmd [dmd and rdmd options] progfile[.d] [program arguments]` builds the file and, transitively, the modules it imports, recompiles only when needed, and runs the result.
- Shebang: first line `#!/usr/bin/env rdmd` then run `./script.d`; on Windows use `#!rdmd` (assuming rdmd is on the path).
- Options: `--eval=code` (code is placed in `void main(string[] args)`; repeatable), `--loop=code` (like `--eval`, inside `foreach (line; stdin.byLine())`), `--main` adds an empty `main`, `--force` rebuild, `--dry-run` shows the commands (implies `--chatty`), `--chatty`, `--compiler=` chooses the compiler, dmd options such as `-O -release` pass through, `--build-only` does not run, `--tmpdir`, `--exclude`/`--include`, `--extra-file`.
- Unit test a module quickly: `rdmd -unittest --main mod.d`.
- With dub packages: `dub run --single script.d` (inline recipe) replaces rdmd when dependencies are needed.
- Two invocations in sequence without a change to any relevant source file do not produce the executable again.

Verify: `rdmd hello.d` twice; the second run does not rebuild.

## Checked

Date 2026-11-02. Confirmed rdmd usage, shebang, --eval, --loop, --main, --force, --dry-run, --compiler and related options (rdmd page). Removed the default-imports claim for --eval, chmod and unverified gotchas.

Method: documentation only; no commands were run.

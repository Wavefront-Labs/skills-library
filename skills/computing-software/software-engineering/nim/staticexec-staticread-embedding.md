---
id: computing-software.software-engineering.nim.staticexec-staticread-embedding
name: staticexec-staticread-embedding
category: computing-software
field: software-engineering
product: nim
tags: [staticexec-staticread-embedding, compile-time-evaluation, staticread, staticexec, embed, gorge, slurp, compile-time-io, resource-embedding, nim]
level: advanced
status: docs-checked
description: "Embed data at compile time in Nim with staticRead (slurp), staticExec (gorge), gorgeEx, cache and --forceBuild, plus CompileDate and CompileTime."
sources:
  - https://nim-lang.org/docs/system.html
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/nimc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# staticRead and staticExec

Goal: bake files and build info into the binary.

- `staticRead(filename)` (alias `slurp`) reads a file at compile time into a string constant. Size is limited by available memory.
- `staticExec(command, input = "", cache = "")` (alias `gorge`) runs a command at compile time and returns its output; `gorgeEx` returns `(output, exitCode)`.
- When `cache` is non-empty the result is cached in nimcache; use `--forceBuild` to bypass.
- Example: `const buildInfo = "Revision " & staticExec("git rev-parse HEAD")`.
- `CompileDate` and `CompileTime` constants give the build timestamp.

Gotchas:
- Execution happens on the build machine, so the command must exist there.

Verify: the binary prints the embedded value.

## Checked

2026-11-03. Confirmed in system docs and the manual. Removed: "path relative to the module", "touch the module to rebuild" and "slow compile" claims.
Method: documentation only; no commands were run.

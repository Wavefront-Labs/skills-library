---
id: computing-software.software-engineering.nim.release-vs-danger-builds
name: release-vs-danger-builds
category: computing-software
field: software-engineering
product: nim
tags: [release-vs-danger-builds, build-optimization-flags, release, danger, debug, checks, boundchecks, optimization, d-release, d-danger, nim]
level: practitioner
status: docs-checked
description: "Choose between debug, release and danger builds, know which runtime checks each removes and their safety trade-offs."
sources:
  - https://nim-lang.org/docs/nimc.html
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# -d:release versus -d:danger

Goal: pick the correct build mode.

- Default (debug): runtime checks and stack traces on, optimizer off.
- `-d:release`: turns on the optimizer; the runtime checks stay on (the define table in the compiler guide lists only the optimizer for `release`).
- `-d:danger`: turns off all runtime checks and turns on the optimizer. Use only on tested hot paths or whole programs verified under release.
- Fine control: `--checks:on|off` (all runtime checks), `--boundChecks`, `--overflowChecks`, `--rangeChecks`, `--assertions`, `--stackTrace` (each `:on|off`), or `{.push boundChecks: off.}` regions. `--nilChecks` is a no-op in current compilers.
- `--opt:none|speed|size` selects the optimisation goal; the option help says to use `-d:release` for a release build.

Gotchas:
- Bugs hidden by danger may only appear there; test with release and sanitizers first.
- Bench with the same flags you ship.

Verify: `nim c --listCmd -d:danger x.nim` shows different C flags from a default build.

## Checked

2026-11-02. Confirmed against nimc.md (define table: `release`, `danger`), basicopt.txt and advopt.txt (`--checks`, `--opt`, `--boundChecks`, `--overflowChecks`, `--rangeChecks`, `--assertions`, `--stackTrace`) and manual.md (`push boundChecks`). Removed: claims that release keeps bounds/overflow/nil checks and enables inlining, the `-O3`/`-O0` figures, the IndexDefect behaviour. Fixed: `--nilChecks` is a no-op in compiler/commands.nim.
Method: documentation only; no commands were run.

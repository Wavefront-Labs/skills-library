---
id: computing-software.software-engineering.nim.coverage-sanitizers-ci
name: coverage-sanitizers-ci
category: computing-software
field: software-engineering
product: nim
tags: [coverage-sanitizers-ci, unit-testing, coverage, gcov, lcov, sanitizers, ci, github-actions, setup-nim, tests, nim]
level: advanced
status: docs-checked
description: "Pass coverage or sanitizer flags to the C compiler, set up Nim in GitHub Actions with setup-nim-action or install-nim, and check formatting with nph --check."
sources:
  - https://nim-lang.org/docs/nimc.html
  - https://github.com/jiro4989/setup-nim-action
  - https://github.com/iffy/install-nim
  - https://github.com/arnetheduck/nph
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coverage, sanitizers and CI for Nim

Goal: automated quality gates.

- Nim compiles through a C compiler. Options reach it with `--passC:OPTION` and `--passL:OPTION`; `--debugger:native` uses the native debugger (gdb) and `--lineDir:on` emits `#line` directives into the generated C, which helps GDB. `-d:useMalloc` makes Nim use C `malloc` (works with `--mm:none`, `--mm:arc` and `--mm:orc`). Which coverage or sanitizer flags your C compiler takes is outside the Nim docs: look them up in the C compiler's manual and pass them through `--passC`/`--passL`.
- GitHub Actions, option 1: `jiro4989/setup-nim-action@v2` with `nim-version` (default `stable`; patterns such as `2.0.x` or `2.x` pick the latest patch or minor), optional `repo-token`; its README example then runs `nimble build -Y` and `nimble test -Y`. The README has sections on cache and `devel` usage.
- Option 2: `iffy/install-nim@v5`; its README runs `nimble install -y` and `nimble test`, and a matrix of `version:` values (for example `binary:stable`, `devel`, `1.4.0`) across `os:` runners.
- Lint steps: `nimble check`; `nph --check file.nim` exits non-zero when a file is not formatted (from the nph README).

Gotchas:
- Action inputs and versions change; read the action README for the version you pin.
- Sanitized builds are slower; run them on a subset of tests.

Verify: the CI run shows tests passing.

## Checked

2026-11-03. Confirmed: Nim compiler guide options above; setup-nim-action README (v2, `nim-version`, `repo-token`, patch/minor patterns, nimble build/test usage); install-nim README (v5, `version` matrix with `devel`, `nimble install -y`, `nimble test`); nph README (`--check`). Removed: gcov/lcov/genhtml recipe, sanitizer flag strings, `nimpretty --check` (nimpretty has no such option), and the cache-key advice (README shows its own cache recipe).
Method: documentation only; no commands were run.

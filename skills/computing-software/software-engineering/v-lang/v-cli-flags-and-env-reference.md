---
id: computing-software.software-engineering.v-lang.v-cli-flags-and-env-reference
name: v-cli-flags-and-env-reference
category: computing-software
field: software-engineering
product: v-lang
tags: [v-cli-flags-and-env-reference, v-cli-maintenance, v flags, compiler flags, -w, -check, -stats, vflags, vmodules, environment variables, v-lang]
level: practitioner
status: draft
description: "Reference the most-used v flags (-g, -prod, -cc, -os, -b, -d, -w, -W, -check, -stats) and key environment variables."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Useful compiler flags and environment variables

Goal: find the right switch quickly.

- `v help` lists subcommands; `v help build` lists compile flags.
- Common: `-prod`, `-g`/`-cg`, `-cc <compiler>`, `-os <target>`, `-b c|js|wasm`, `-d <flag>`, `-o <file>`, `-shared`, `-gc <mode>`, `-autofree`, `-enable-globals`, `-skip-unused`, `-stats`, `-show-timings`, `-keep-c`, `-showcc`.
- Warnings: `-w` suppress, `-W` warnings as errors (confirm), `-check` only type-check (confirm name), `-check-syntax` parse-only.
- Env: `VFLAGS` default flags for every build, `VMODULES` module root, `VEXE` compiler path, `VJOBS` parallel jobs, `VCACHE` cache dir (confirm).
- Place default flags in `VFLAGS="-prod"` for CI builds.

Gotchas:
- Flags must come before the file/dir: `v -prod run app.v`.
- `VFLAGS` applies to tests and subcommands too, which may surprise.

Verify: `v -stats test .` and `v -showcc .` both behave.

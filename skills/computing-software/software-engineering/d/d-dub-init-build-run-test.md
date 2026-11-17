---
id: computing-software.software-engineering.d.d-dub-init-build-run-test
name: d-dub-init-build-run-test
category: computing-software
field: software-engineering
product: d
tags: [d-dub-init-build-run-test, dub-commands, dub, dub-init, dub-build, dub-run, dub-test, dub-describe, dub-lint, dub-single-file, compiler-option, arch, d]
level: intro
status: docs-checked
description: "Use the core dub commands: init, build, run, test, lint, describe, clean, --compiler, --arch, -b/-c, --force, --rdmd single-file scripts, and verbosity flags."
sources:
  - https://dub.pm/dub-guide/single/
  - https://dub.pm/dub-reference/dub_home/
  - https://dub.pm/dub-reference/build_settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dub init, build, run, test, lint, describe and common options

Goal: day-to-day dub usage.

- New: `dub init myapp` (interactive; `-t minimal` (default), `-t vibe.d`, `-t deimos` or `-t custom`; `-f|--format` selects the recipe format, `-n` non-interactive).
- Build/run: `dub build [-b release] [-c config] [--compiler=ldc2] [--arch=x86_64] [--force] [-q|-v|--vquiet]`; `dub run -- args` passes arguments to the program; `dub run -b release`; `dub build --combined` tries to build the whole project in a single compiler run.
- Test: `dub test` / `dub test --coverage`.
- Inspect: `dub describe` (json of settings, `--data=import-paths`), `dub list`, `dub search term`, `dub lint` (dscanner), `dub build --nodeps`, `dub dustmite`, `dub generate visuald|sublimetext|cmake` (project files), `dub convert`.
- Single-file script: first line `/+ dub.sdl: dependency "silly" version="*" +/` in `app.d` then `dub app.d` or `dub --single app.d`; shebang `#!/usr/bin/env dub`. `dub app.d` and `./app.d` rebuild on every invocation; `dub build --single app.d` produces a reusable executable.
- User packages and cache: `~/.dub/packages`, `~/.dub/cache` (override with `DUB_HOME`/`DPATH`); `dub clean-caches`.
- Colour: `--color=auto|always|never`.
- `--arch` (`-a`) forces a different architecture (e.g. x86, x86_64, aarch64).

Verify: `dub init -n demo && cd demo && dub run`.

## Checked

Date 2026-11-02. Confirmed init templates and formats, build, run, test, single-file packages and DUB_HOME cache locations (dub docs; CLI flags checked in dub commandline.d). Error fixed: -t library is not an init template. Removed dub test filter, x86_mscoff and exit-code claims.

Method: documentation only; no commands were run.

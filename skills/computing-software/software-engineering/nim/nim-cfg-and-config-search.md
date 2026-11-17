---
id: computing-software.software-engineering.nim.nim-cfg-and-config-search
name: nim-cfg-and-config-search
category: computing-software
field: software-engineering
product: nim
tags: [nim-cfg-and-config-search, configuration-files, nim-cfg, config, switches, path, define, conditional, config-search-order, nim]
level: practitioner
status: docs-checked
description: "Where the Nim compiler reads nim.cfg and config.nims from, in what order, how to skip each level, and how to inspect the result with nim dump and --listCmd."
sources:
  - https://nim-lang.org/docs/nimc.html
  - https://nim-lang.org/docs/nims.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nim.cfg and config search order

Goal: persist compiler options.

- The compiler guide lists, in order (later files overwrite earlier settings): the global `$nim/config/nim.cfg` (`/etc/nim/nim.cfg` on UNIX, install dir `config\nim.cfg` on Windows; skip with `--skipCfg`); the user file `$XDG_CONFIG_HOME/nim/nim.cfg` or `~/.config/nim/nim.cfg` (`%APPDATA%/nim/nim.cfg` on Windows; `--skipUserCfg`); `nim.cfg` in any parent directory of the project file (`--skipParentCfg`); `nim.cfg` in the project directory (`--skipProjCfg`); and `$project.nim.cfg` next to `$project.nim` (also skipped by `--skipProjCfg`).
- NimScript files can also configure the compiler: `config.nims` in the user config dir, parent directories and the project directory, plus `$project.nims` next to `$project.nim`.
- Command-line settings take priority over configuration files.
- Path-valued options support `$nim`, `$lib`, `$home` / `~`, `$config`, `$projectname`, `$projectpath` / `$projectdir`, `$nimcache`.
- Cross-compilation settings in config files use lines like `arm.linux.gcc.path = "/usr/bin"` and `arm.linux.gcc.exe = "arm-linux-gcc"` (from the guide's example).
- `nim dump` shows all defined conditionals and search paths (`--dump.format:json` for JSON); `--listCmd` lists the compilation commands.

Gotchas:
- A `nim.cfg` in a parent directory of the project file applies to that project and silently changes its settings; check with `nim dump`.

Verify: `nim dump` shows your path entry.

## Checked

2026-11-03. Confirmed in the compiler guide (load order, skip options, path substitutions, cross-compilation example, `dump`, `--listCmd`) and the NimScript page (config.nims locations). Removed: `@if/@else/@end` syntax, `cc = gcc`, `--mm:orc` example lines in nim.cfg, `<project>.nim.cfg`-only-when-compiling claim, quoting rule, and the "tests dir" gotcha.
Method: documentation only; no commands were run.

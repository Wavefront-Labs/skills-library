---
id: computing-software.software-engineering.nim.config-nims-switch-api
name: config-nims-switch-api
category: computing-software
field: software-engineering
product: nim
tags: [config-nims-switch-api, configuration-files, config-nims, nimscript, switch, task, when-defined, build-config, project-config, nim]
level: practitioner
status: docs-checked
description: "Write config.nims with the switch API and -- templates, define tasks, know the config load order, skip flags and NimScript limits."
sources:
  - https://nim-lang.org/docs/nims.html
  - https://nim-lang.org/docs/nimscript.html
  - https://nim-lang.org/docs/nimc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# config.nims and the switch API

Goal: scriptable, conditional configuration.

```nim
# config.nims
switch("opt", "size")
switch("path", "$projectDir/../src")
when defined(windows):
  switch("define", "release")
--threads:on
```
- `switch("FOO")` equals `--FOO`, and `switch("FOO", "VAL")` equals `--FOO:VAL`. The `--opt:size` style can be written as-is in the file.
- `-d:strip`, `-d:lto` and `-d:lto_incremental` cannot be set from NimScript.
- Path options accept the substitutions `$nim`, `$lib`, `$home`, `$config`, `$projectname`, `$projectpath`/`$projectdir` and `$nimcache`.
- Available procs from the nimscript module include `exec`, `getEnv`, `fileExists`, `thisDir`, `projectDir`, `projectName`, `withDir`, `setCommand`; `exec` raises `OSError` on failure, and `system.gorgeEx` returns the exit code and output.
- `task name, "description":` defines a task; the NimScript page lists conventional task names `help`, `build`, `tests`, `bench`. Example: `task build, "builds an example": setCommand "c"`.
- Load order (later overrides earlier): `~/.config/nim/config.nims` (or `$XDG_CONFIG_HOME/nim/config.nims`; `%APPDATA%/nim/config.nims` on Windows), `config.nims` in any parent directory of the project file, `config.nims` in the project directory, then `$project.nims` next to `$project.nim`. Skip them with `--skipUserCfg`, `--skipParentCfg` and `--skipProjCfg`. Command-line settings win over configuration files.
- `nim myscript.nims` runs a NimScript file standalone.

Gotchas:
- NimScript runs in the VM: no FFI, so any stdlib module relying on `importc` is unavailable, and only a listed subset of the stdlib works.
- `nim dump` shows the defined symbols and search paths after configuration.

Verify: `nim dump` reflects switches set in config.nims.

## Checked

2026-11-03. Confirmed in the NimScript page (switch, `--` templates, strip/lto restriction, tasks, load order, limitations, standalone `nim myscript.nims`), the nimscript module page (`exec`, `getEnv`, `fileExists`, `thisDir`, `projectDir`, `projectName`, `withDir`, `setCommand`) and the compiler guide (substitutions, skip flags, `dump`). Removed: `existsFile`, `execProcess` advice, `nim name file.nim` / `nimble name` task invocation, `hostOS`, `-flto` example, "`<module>.nims` loads only for that module".
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.crystal.shards-postinstall-build
name: shards-postinstall-build
category: computing-software
field: software-engineering
product: crystal
tags: [shards-postinstall-build, shards, postinstall, shards-build, scripts, executables, targets, bin, shards-run, native-extension, crystal]
level: advanced
status: docs-checked
description: "Shards postinstall scripts, executables and targets: shards build and shards run, --skip-postinstall and --skip-executables, where binaries land in bin."
sources:
  - https://github.com/crystal-lang/shards/blob/master/docs/shard.yml.adoc
  - https://github.com/crystal-lang/shards/blob/master/docs/shards.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# postinstall, scripts and building targets

Goal: build native parts and the app.

```yaml
scripts:
  postinstall: cd src/libfoo && make
executables:
  - mytool
targets:
  mytool:
    main: src/cli.cr
```
- `postinstall` runs whenever the dependency is installed or upgraded in a project that requires it, from the dependency's install directory (for example `lib/foo`). Use it to compile a C library or build tools. `scripts` supports only `postinstall`.
- `shards install --skip-postinstall` skips dependency postinstall scripts; `--skip-executables` skips installing executables.
- `shards build [targets] [build_options]` builds the named targets (all if none) into `bin`; it ensures dependencies are installed first, and all options after the command are passed to `crystal build`.
- `shards run [target] [-- options]` builds and runs a target; with no target, runs the only target if `shard.yml` defines exactly one. Arguments after `--` go to the target process.
- A target's key is the binary name created in the project's `bin`; `main` is the source file.
- `executables:` files must exist in the shard's `bin` folder with the executable bit (POSIX); they are copied into a dependent project's `bin`, installed after `postinstall`, so a library can build them there.

Gotchas:
- Postinstall scripts are shell commands from dependencies; review them before installing untrusted shards.

Verify: the built target appears under `bin`.

## Checked

2026-11-03. Confirmed against shard.yml(5) (`scripts`, `postinstall`, `executables`, `targets`) and shards(1) (`build`, `run`, `install` options).
Removed: the flags `--release` and `--static` written into the synopsis (only "delegated to crystal build" is documented), "Windows support differs", and the uncertain "(confirm)" notes now resolved: `shards run` exists in the man page.
Method: documentation only; no commands were run.

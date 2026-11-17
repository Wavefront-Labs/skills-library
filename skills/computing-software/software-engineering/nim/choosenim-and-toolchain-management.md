---
id: computing-software.software-engineering.nim.choosenim-and-toolchain-management
name: choosenim-and-toolchain-management
category: computing-software
field: software-engineering
product: nim
tags: [choosenim-and-toolchain-management, editor-tooling, choosenim, install-nim, toolchain, nim-version, grabnim, asdf, nim-devel, update, nim]
level: intro
status: docs-checked
description: "Install Nim via choosenim, switch between stable and devel toolchains, and know where it puts proxies and toolchains."
sources:
  - https://github.com/nim-lang/choosenim
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing and switching Nim versions with choosenim

Goal: manage compilers.

- Unix install: `curl https://nim-lang.org/choosenim/init.sh -sSf | sh` (or the `wget -qO - ... | sh` form). Set `CHOOSENIM_CHOOSE_VERSION` to pick the initial version the script installs.
- Windows: download the .zip from the choosenim GitHub releases page, extract it and run `runme.bat`. A Windows C compiler is downloaded automatically; on Linux and macOS you need gcc or clang.
- Use: `choosenim stable` (latest stable release), `choosenim 1.6.6` (a version number), `choosenim "#head"` (latest commit; quote it in the shell), `choosenim ~/projects/nim` (an existing installation).
- `choosenim update stable` updates the stable channel; `choosenim update self` updates choosenim; `choosenim show` prints the selected version and channel (`show path` prints only the path); `choosenim versions [--installed]` lists versions.
- Channels: `stable` (latest stable release) and `devel` (latest development or nightly release from the devel branch).
- How it works: choosenim is a toolchain multiplexer. `nim`, `nimble` and other tools in `~/.nimble/bin` are proxies; toolchains live in `~/.choosenim/toolchains`. Directories can be changed with `--choosenimDir:<dir>` and `--nimbleDir:<dir>`.
- Installed components on `choosenim stable` include nim, nimble, nimgrep, nimpretty, nimsuggest and testament.
- Official binaries are installed on Windows and Linux; other platforms download the source release and build it (once per new version).

Gotchas:
- Git is required for `#HEAD` or a specific commit; selecting branches likely needs Nim to be bootstrapped, which may be slow.
- Make sure `~/.nimble/bin` is on `PATH`, otherwise the proxies are not found.

Verify: `nim -v` prints the chosen version.

## Checked

2026-11-08. Read in full: the choosenim README (nim-lang/choosenim): install commands, usage text, channels, dependency table, how toolchains and proxies are laid out. Removed: grabnim, asdf-nim, Docker image and OS package manager alternatives, the claim that development has slowed, and `requires "nim == x"` pinning (none confirmed in the README); the nim-lang.org manual, tutorial and library pages were not relevant and are dropped from sources.
Method: documentation only; no commands were run.

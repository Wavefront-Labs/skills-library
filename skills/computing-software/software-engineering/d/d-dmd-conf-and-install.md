---
id: computing-software.software-engineering.d.d-dmd-conf-and-install
name: d-dmd-conf-and-install
category: computing-software
field: software-engineering
product: d
tags: [d-dmd-conf-and-install, dmd-compiler, install-dmd, dmd-conf, sc-ini, dflags, install-sh, dlang-installer, version-manager, path, d]
level: practitioner
status: draft
description: "Install DMD/LDC/GDC with install.sh, choco/apt/brew or installers, understand dmd.conf and sc.ini search paths, DFLAGS, and managing versions with the install script."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Installing D, dmd.conf / sc.ini and DFLAGS

Goal: set up and switch compilers.

- Official script: `curl -fsS https://dlang.org/install.sh | bash -s dmd` (or `ldc`, `gdc`, `dmd-2.109.1`); then `source ~/dlang/dmd-*/activate`; `deactivate` restores. Windows: the installer exe or `choco install dmd`; macOS `brew install dmd ldc dub`; Debian `apt install gdc ldc` (distribution versions can be old; confirm).
- Config: `dmd.conf` (POSIX: next to the binary, `/etc/dmd.conf`, `~/.dmd.conf`) or `sc.ini` (Windows, in the `bin` dir) holds `DFLAGS=-I%@P%/../../src/phobos -L-L%@P%/../lib64`; override per-run with the `DFLAGS` environment variable or command line.
- Check: `dmd --version`, `dub --version`, `ldc2 --version`, `echo $DFLAGS`.
- Multiple compilers with dub: `dub build --compiler=ldc2` or env `DC=ldc2`.
- Windows toolchain: MSVC build tools / Windows SDK needed for 64-bit linking (dmd installer offers VS Build Tools).
- Language server and editors: `serve-d`, code-d (VS Code), dlang-vscode extension (confirm current names).

Gotchas:
- A stale `dmd` earlier in PATH hides the one you just installed; check `which dmd` / `where dmd`.
- Mixing druntime/phobos from different versions causes link errors.

Verify: build and run a hello world, then print `dmd --version`.

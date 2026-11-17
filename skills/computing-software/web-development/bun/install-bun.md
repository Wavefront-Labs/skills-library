---
id: computing-software.web-development.bun.install-bun
name: install-bun
category: computing-software
field: web-development
product: bun
tags: [bun-install-methods, install-script, verify-version, command-not-found, uninstall]
level: intro
status: docs-checked
description: "Install Bun with the install script, npm, Homebrew, Scoop or Docker, verify it, fix command-not-found PATH problems, and meet the OS and CPU requirements."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/installation.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install:

```bash
curl -fsSL https://bun.com/install | bash      # macOS/Linux
powershell -c "irm bun.sh/install.ps1|iex"      # Windows
npm install -g bun
brew install oven-sh/bun/bun
scoop install bun
docker pull oven/bun
```

Verify with `bun --version` (version) and `bun --revision` (exact commit).

Requirements and traps:
- Linux: install `unzip` first; kernel 5.6+ is recommended. glibc binaries need glibc 2.17+; on a `GLIBC_... not found` error use the musl binary (Alpine, Void).
- Windows 10 version 1809 or later; macOS 13.0 or later.
- x64 CPUs must support SSE4.2 (Intel Nehalem or newer, AMD Bulldozer or newer). The `-baseline` assets are only aliases of the same binary.
- "command not found" usually means `~/.bun/bin` is not on PATH. Add `BUN_INSTALL` and the PATH export to `~/.bashrc`, `~/.zshrc` or fish config, then reload the shell.
- Windows: if `& "$env:USERPROFILE\.bun\bin\bun" --version` works, add `~\.bun\bin` to the user PATH and restart the terminal.

Uninstall: `rm -rf ~/.bun`, or use the package manager that installed it (`npm uninstall -g bun`, `brew uninstall bun`, `scoop uninstall bun`).

## Checked

2026-11-04. Confirmed against bun docs installation.mdx: install commands, bun --version and --revision, Linux unzip and kernel 5.6, glibc 2.17 and musl, Windows 1809, macOS 13, SSE4.2 CPU floor, -baseline aliases, PATH fixes, uninstall. Added the Windows 10 wording.

Method: documentation only; no commands were run.

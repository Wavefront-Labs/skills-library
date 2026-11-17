---
id: computing-software.software-engineering.pnpm.install-pnpm
name: install-pnpm
category: computing-software
field: software-engineering
product: pnpm
tags: [install-pnpm, self-update, standalone-installer, get-pnpm, supported-platforms, pnpm-version-env, node-compatibility, windows-defender-exclusion]
level: intro
status: docs-checked
description: "Install and update pnpm 12: self-update, standalone scripts for Windows and POSIX, PNPM_VERSION, npx get-pnpm, npm install, platforms, Node.js compatibility, PATH fixes."
sources:
  - https://pnpm.io/installation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
pnpm 12 is a native executable and needs no Node.js after install. The `pnpm` npm package needs Node.js 18+; `npx get-pnpm` needs Node.js 22.13+.

Install paths:
- From pnpm v11.10.0+: `pnpm self-update`. Inside a project pinned by `packageManager`, it updates only that pin.
- POSIX: `curl -fsSL https://get.pnpm.io/install.sh | sh -` (or `wget -qO- ... | sh -`); pin with `env PNPM_VERSION=<version> sh -`. In Docker use `env ENV="$HOME/.bashrc" SHELL="$(which bash)" bash -` (similarly sh, dash).
- Windows PowerShell: `Invoke-WebRequest https://get.pnpm.io/install.ps1 -UseBasicParsing | Invoke-Expression`. Defender may block the executable, so installing with npm is recommended on Windows. Speed up installs with `Add-MpPreference -ExclusionPath $(pnpm store path)`.
- npm: `npx get-pnpm` or `npm install -g pnpm@latest`.
- Use `pnpm runtime` afterwards to install Node.js.

Prebuilt binaries: Linux glibc (x64, arm64, riscv64, ppc64le, s390x), Linux musl (x64, arm64), macOS (arm64, x64), Windows (x64, arm64), FreeBSD x64, Android (arm64, x64). FreeBSD, ppc64le, s390x, RISC-V and Android arrived in v12.4.0; otherwise install the JavaScript pnpm 11. Node.js 18 and 20 work with pnpm 10 and 12 but not 11; 22, 24 and 26 work with all three.

Broken install: find it with `which pnpm` (Windows `where.exe pnpm.*`) and delete leftover `pnpm`, `pnpm.cmd`, `pnpx.cmd` files that shadow it, then reinstall.

## Checked

2026-11-04. Confirmed against pnpm.io/installation: native executable and Node.js requirements, self-update from v11.10.0, standalone scripts and Docker variants, PNPM_VERSION, Windows Defender notes, npm installers, platform list and v12.4.0 additions, Node.js compatibility table, PATH troubleshooting. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.pnpm.pnx-run-package
name: pnx-run-package
category: computing-software
field: software-engineering
product: pnpm
tags: [pnx, pnpm-dlx, pnpx, run-without-installing, package-flag, allow-build-pnx, silent-run]
level: practitioner
status: docs-checked
description: "Run a registry package once without installing it using pnx (aliases pnpm dlx, pnpx): versions, --package, catalog: specifiers, build approvals, shell mode, trust policies."
sources:
  - https://pnpm.io/cli/pnx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`pnx` fetches a package without adding it as a dependency, hotloads it and runs its default binary. Aliases: `pnpm dlx`, `pnpx`.

```sh
pnx create-vue my-app
pnx create-vue@next my-app
pnx shx@catalog:                       # version from a workspace catalog
pnx --package=@pnpm/meta-updater meta-updater --help
pnx --package=yo --package=generator-webapp yo webapp --skip-install
pnx --package cowsay --package lolcatjs -c 'echo "hi pnpm" | cowsay | lolcatjs'
pnx --cpu arm64,x64 --os linux some-cli
```

Options:
- `--package <name>`: package(s) to install before running; repeatable.
- `--allow-build <pkgs>`: dependencies allowed to run build scripts. The package pnx itself executes may build by default. In an interactive terminal pnx prompts to approve skipped builds; approvals are saved in the isolated pnx cache, not your project. Without a terminal, unapproved builds stay skipped.
- `-c` / `--shell-mode`: run inside `/bin/sh` or `cmd.exe`.
- `--cpu`, `--os`, `--libc` (glibc or musl): which platform-tagged optional dependencies to keep.
- `-s` / `--silent`: print only the command's output.

Security: `minimumReleaseAge*` and `trustPolicy*` settings apply, so pnx refuses freshly published or insufficiently trusted packages like a normal install.

## Checked

2026-11-04. Confirmed aliases, catalog: support, --package, --allow-build, --shell-mode, --cpu/--os/--libc, --silent and the minimumReleaseAge and trustPolicy settings against pnpm.io/cli/pnx. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.

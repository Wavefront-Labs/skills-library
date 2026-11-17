---
id: computing-software.software-engineering.pnpm.exec-commands
name: exec-commands
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-exec, shell-mode, pnpm-package-name, exec-recursive, run-installed-binary]
level: practitioner
status: docs-checked
description: "Use pnpm exec to run dependency binaries or shell commands in project scope, in every workspace project with -r, with -c shell mode and PNPM_PACKAGE_NAME."
sources:
  - https://pnpm.io/cli/exec
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`pnpm exec <cmd>` runs a shell command with `node_modules/.bin` on `PATH`; `PNPM_PACKAGE_NAME` holds the current package name.

```sh
pnpm exec jest      # same as: pnpm jest (when not a builtin pnpm command)
pnpm -r exec jest   # every workspace project
pnpm exec -r jest   # same
pnpm exec jest -r   # current project only; -r goes to jest
pnpm -r exec rm -rf node_modules
pnpm -rc exec pnpm view \$PNPM_PACKAGE_NAME
```

pnpm reads its own options up to the command name; everything after is passed to the command.

Options:
- `-r`: all projects; recursive options (`--workspace-concurrency`, `--[no-]sort`, `--reverse`) apply.
- `-c` / `--shell-mode`: run inside a shell (`/bin/sh` on UNIX, `cmd.exe` on Windows); needed for env vars like `$PNPM_PACKAGE_NAME` to expand.
- `--parallel`: ignore concurrency and ordering, for long-running processes.
- `--resume-from <name>`: resume at a project.
- `--no-reporter-hide-prefix`, `--report-summary`, `--filter <selector>`.

## Checked

2026-11-04. Confirmed against pnpm.io/cli/exec: PATH and PNPM_PACKAGE_NAME behaviour, option-position rules and the -r examples, --recursive, --shell-mode, --parallel, --resume-from, --no-reporter-hide-prefix, --report-summary, --filter. Removed: the closing Check line, which restated a point already made in the options.
Method: documentation only; no commands were run.

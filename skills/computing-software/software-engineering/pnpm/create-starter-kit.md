---
id: computing-software.software-engineering.pnpm.create-starter-kit
name: create-starter-kit
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-create, starter-kit, create-package-mapping, dlx, one-off-execution]
level: intro
status: docs-checked
description: "Scaffold a project with pnpm create: how a name maps to a create-* package, extra arguments, --allow-build, and the security policies that apply to the starter kit."
sources:
  - https://pnpm.io/cli/create
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```sh
pnpm create <name> [<args>...]
pnpm create vite my-app
```

Name to package mapping:

| Name | Package |
|---|---|
| `foo` | `create-foo` |
| `create-foo` | `create-foo` |
| `@scope` | `@scope/create` |
| `@scope/foo` | `@scope/create-foo` |

pnpm runs the starter kit with `pnx` and passes the remaining arguments to it.

Options: `--allow-build` (packages allowed to run postinstall scripts), `-c` / `--shell-mode` (run in `/bin/sh` or `cmd.exe`), plus `--cpu`, `--os`, `--libc` platform overrides.

Security: `pnpm create` honours project-level `minimumReleaseAge`, `minimumReleaseAgeExclude`, `minimumReleaseAgeStrict`, `trustPolicy`, `trustPolicyExclude` and `trustPolicyIgnoreAfter` when resolving and fetching the starter kit. See `computing-software.software-engineering.pnpm.minimum-release-age`.

## Checked

2026-11-04. Confirmed against pnpm.io/cli/create: name-to-package table, pnx runner, example, --allow-build, --shell-mode, --cpu/--os/--libc, the six honoured security settings. Removed: the parenthetical about a dlx docs page being unavailable and the generic closing Check line.
Method: documentation only; no commands were run.

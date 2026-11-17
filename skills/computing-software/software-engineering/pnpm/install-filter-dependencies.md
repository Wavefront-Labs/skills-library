---
id: computing-software.software-engineering.pnpm.install-filter-dependencies
name: install-filter-dependencies
category: computing-software
field: software-engineering
product: pnpm
tags: [prod-install, dev-only-install, no-optional, no-runtime, dry-run, lockfile-only, ignore-workspace]
level: practitioner
status: docs-checked
description: "Choose pnpm install modes: --prod, --dev, --no-optional, --no-runtime, --dry-run, --lockfile-only, --offline, --ignore-workspace and --lockfile-dir, with the lockfile caveats."
sources:
  - https://pnpm.io/cli/install
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
| Flag | Effect |
|---|---|
| `--prod`, `-P` | skip `devDependencies` (and remove them if installed) |
| `--dev`, `-D` | install only `devDependencies` |
| `--no-optional` / `--optional` | skip / force `optionalDependencies` |
| `--no-runtime` | skip runtime entries such as Node from `devEngines.runtime`; lockfile untouched |
| `--dry-run` | full resolution, report changes, write nothing (exit 0) |
| `--lockfile-only` | update `pnpm-lock.yaml` and `package.json` only |
| `--offline` / `--prefer-offline` | store only / skip staleness checks |
| `--ignore-workspace` | treat project as standalone |
| `--lockfile-dir <dir>` | where the lockfile lives; shareable, not with `--global` |

Caveats:
- Without a lockfile, pnpm must still produce a consistent one, so `--prod` still resolves dev dependencies (except `link:` ones).
- Without `--frozen-lockfile`, `file:` dependencies are rechecked, so a removed target errors.
- `--no-runtime` suits CI matrices where Node is provisioned first.
- `recursiveInstall: false` stops workspace-wide installs.

## Checked

2026-11-04. Confirmed against pnpm.io/cli/install: flag table (--prod, --dev, --optional, --no-runtime, --dry-run, --lockfile-only, offline flags, --ignore-workspace, --lockfile-dir), lockfile-less and file: caveats, recursiveInstall. Removed: the generic closing Check line (a git status claim not on the page).
Method: documentation only; no commands were run.

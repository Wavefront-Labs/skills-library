---
id: computing-software.software-engineering.pnpm.ci-install-pnpm
name: ci-install-pnpm
category: computing-software
field: software-engineering
product: pnpm
tags: [continuous-integration, ci, standalone-script, pnpm-setup-action, corepack-warning, ci-frozen-lockfile]
level: practitioner
status: docs-checked
description: "Install pnpm in CI: official image, get.pnpm.io standalone script with fallback, PNPM_HOME on PATH, pnpm/setup for GitHub Actions, packageManager version, CI lockfile behaviour."
sources:
  - https://pnpm.io/continuous-integration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Options:
- Container CI: use `ghcr.io/pnpm/pnpm` as the job image, then `pnpm runtime set node lts -g`.
- Elsewhere: the standalone script, saved to a file and run only if a download succeeded:

```sh
{ curl -fsSL https://get.pnpm.io/ -o /tmp/pnpm-install.sh \
  || curl -fsSL https://github.com/pnpm/get.pnpm.io/releases/latest/download/install.sh -o /tmp/pnpm-install.sh; } \
  && sh /tmp/pnpm-install.sh
```

- GitHub Actions: `pnpm/setup` with `runtime: node@<ver>` and `cache: true`; it installs pnpm, the runtime and runs `pnpm install` (`install: false` to skip). The pnpm version comes from `packageManager` or `devEngines.packageManager`; add a `version` input if neither exists.

Points:
- Needs no Node.js; pnpm switches to the project's pinned version on first use.
- The script installs into `PNPM_HOME` and edits a shell profile CI never reloads, so set `PNPM_HOME` and put `$PNPM_HOME/bin` on `PATH` yourself.
- Docs say do not use Corepack (a Node shim runs on every call).
- In CI, frozen-lockfile mode is automatic; `--no-frozen-lockfile` opts out; the `ci` setting forces or disables detection. `pnpm ci` runs `pnpm clean` then a frozen install. A lockfile from a newer pnpm major fails instead of being rewritten.

## Checked

2026-11-04. Confirmed against pnpm.io/continuous-integration: official image and pnpm runtime set node lts -g, standalone script command, no Node.js needed, version following packageManager/devEngines, PNPM_HOME/PATH note, Corepack warning, GitHub Actions pnpm/setup behaviour, frozen-lockfile in CI, pnpm ci, newer-major lockfile failure. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.

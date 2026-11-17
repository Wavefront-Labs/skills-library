---
id: computing-software.software-engineering.pnpm.install-update-checksums
name: install-update-checksums
category: computing-software
field: software-engineering
product: pnpm
tags: [update-checksums, tarball-integrity, err-pnpm-tarball-integrity, trust-lockfile, registry-rewrite]
level: advanced
status: docs-checked
description: "Handle ERR_PNPM_TARBALL_INTEGRITY in pnpm: why integrity mismatches fail hard, when --update-checksums is the right opt-in, and what does not bypass the check."
sources:
  - https://pnpm.io/cli/install
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An integrity mismatch between a locked package and the registry tarball is a hard failure: `pnpm install` exits with `ERR_PNPM_TARBALL_INTEGRITY` instead of re-resolving and overwriting the locked integrity. This protects committed lockfiles from a compromised registry, proxy or republished version.

Legitimate case (a registry rewrote its tarballs, or started serving tars, and you have verified the new bytes):

```sh
pnpm install --update-checksums
```

It re-resolves every locked package and records the integrity the registry reports now in `pnpm-lock.yaml`. A warning prints when the bypass applies, so it is auditable.

Not bypasses: `--force`, `pnpm update`, `--frozen-lockfile` (unchanged) and `--fix-lockfile` (only fills in missing lockfile entries).

Related: `--trust-lockfile` skips verifying the lockfile against supply-chain policies; `--no-trust-lockfile` verifies even when configuration trusts it.

## Checked

2026-11-04. Confirmed against pnpm.io/cli/install: ERR_PNPM_TARBALL_INTEGRITY hard failure, --update-checksums behaviour and warning, non-bypasses, --trust-lockfile and --no-trust-lockfile. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.

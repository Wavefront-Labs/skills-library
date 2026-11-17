---
id: computing-software.software-engineering.pnpm.audit-vulnerabilities
name: audit-vulnerabilities
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-audit, audit-fix, audit-level, audit-ignore, ghsa, audit-ignore-prune, audit-json]
level: practitioner
status: docs-checked
description: "Run pnpm audit: severity levels and exit codes, --fix as overrides or update, ignoring advisories by GHSA ID, audit.ignorePrune, scope flags and registry-error handling."
sources:
  - https://pnpm.io/cli/audit
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`pnpm audit` queries the registry's `/-/npm/v1/security/advisories/bulk`. Advisories are identified by GHSA ID (no CVEs in the response). Exit code 1 when an advisory at or above the audit level remains after ignores.

Fixing: try `pnpm update`; else force versions with overrides, e.g. `overrides: { "lodash@<2.1.0": "^2.1.0" }`, or run `pnpm audit --fix` (writes overrides to `pnpm-workspace.yaml`). `--fix=update` updates the lockfile instead. With `minimumReleaseAge` set, `--fix` also adds the patched version to `minimumReleaseAgeExclude`. `-i` reviews fixes and implies `--fix=override`.

Config in `pnpm-workspace.yaml`:

```yaml
audit:
  level: high            # info, low (default), moderate, high, critical
  ignore:
    - GHSA-42xw-2xvc-qx8m
  ignorePrune: true      # v12.0.0: --fix drops ignores no longer in the report
```

Flags: `--audit-level`, `--json` (`patched_versions` is null when no fix exists), `--dev`, `--prod`, `--optional` (default) / `--no-optional`, `--ignore <GHSA>` (saved to config), `--ignore-unfixable` (unfixable advisory with no GHSA fails with `ERR_PNPM_AUDIT_MISSING_GHSA`), `--ignore-registry-errors` (non-200 exits 0).

Since v12.4.0 ignored advisories are reported separately from totals. Deprecated: `auditLevel`, `auditConfig.ignoreGhsas` (the `audit` section wins with a warning). `auditConfig.ignoreCves` is not recognised.

## Checked

2026-11-04. Confirmed against pnpm.io/cli/audit: bulk advisories endpoint, GHSA identification, exit code, --fix variants, minimumReleaseAgeExclude, audit.level/ignore/ignorePrune config, flags, ERR_PNPM_AUDIT_MISSING_GHSA, v12.4.0 reporting, deprecated names. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.

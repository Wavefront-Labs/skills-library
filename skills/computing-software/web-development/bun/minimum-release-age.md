---
id: computing-software.web-development.bun.minimum-release-age
name: minimum-release-age
category: computing-software
field: web-development
product: bun
tags: [minimum-release-age, supply-chain, release-cooldown]
level: advanced
status: docs-checked
description: "Delay adoption of freshly published npm versions with --minimum-release-age and its excludes list, and know which installs bypass the check."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/install.mdx
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/audit.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--minimum-release-age N` ignores versions younger than N seconds; units such as `3d` are accepted. `--minimum-release-age-excludes` exempts packages and replaces the config list.

```bash
bun install --minimum-release-age 259200 \
  --minimum-release-age-excludes @types/node,typescript@5.4.5
```

Persistent form in `bunfig.toml` under `[install]`: `minimumReleaseAge` and `minimumReleaseAgeExcludes`.

Gotchas:
- It affects only new resolution. Requesting an exact version bypasses the stability check.
- Versions already in the lockfile are not re-evaluated.
- `bun audit fix` may still install a safe version newer than the cooldown; it marks such rows `(newer than --minimum-release-age)`.
- The excludes flag replaces, not extends, the configured list.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/install.mdx and pm/cli/audit.mdx: seconds and unit values, excludes flag replacing the config list, bunfig keys, new-resolution-only scope, stability-check bypass for exact versions, audit fix marker text. Removed an unsourced Verify line.

Method: documentation only; no commands were run.

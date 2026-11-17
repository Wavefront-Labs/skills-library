---
id: computing-software.devops-ci-cd.verdaccio.release-age-gate-and-private-scope
name: release-age-gate-and-private-scope
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [release-age, minimum-release-age, supply-chain, min-release-age, npmminimalagegate, enoversions, newly-published]
level: advanced
status: docs-checked
description: "Fix newly published private versions looking missing because pnpm, Yarn or npm release-age gates hide them, with per-client settings and units."
sources:
  - https://verdaccio.org/docs/cli-registry/
  - https://verdaccio.org/docs/setup-pnpm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Recent versions are hidden by default on pnpm and Yarn as a supply-chain precaution. Against a private registry the package you just published looks absent, and the error says the version does not exist.

| Client | Setting | Unit | Default | Exempt own scope |
|---|---|---|---|---|
| pnpm | `minimumReleaseAge` | minutes | 1440 since pnpm 11 | `minimumReleaseAgeExclude` |
| Yarn | `npmMinimalAgeGate` | minutes, accepts `1d` | `1d` since 4.15 | `npmPreapprovedPackages`, or per scope |
| npm | `min-release-age` | days | off (null), still in npm 12 | `min-release-age-exclude` |

Units differ: `1` is one day in npm but one minute in pnpm and Yarn.

Examples:
```yaml
# pnpm-workspace.yaml
minimumReleaseAge: 1440
minimumReleaseAgeExclude:
  - '@my-company/*'
```
```
# .npmrc (npm)
min-release-age=7
min-release-age-exclude[]=@my-company/*
```
```yaml
# .yarnrc.yml
npmPreapprovedPackages:
  - '@my-company/*'
```
Errors: pnpm `No matching version found for ...`; npm `ENOVERSIONS`. One-off: `npm install <pkg> --min-release-age=0`. pnpm has no CLI flag or env var; use `pnpm config set minimumReleaseAge 0 --location=project`. Yarn also quarantines a version whose publish date it cannot read, so a storage plugin dropping `time` would block installs.

`npm audit fix` can be blocked by the gate and exits non-zero.

## Checked

2026-11-04. Confirmed against the Verdaccio Using a private registry, pnpm, npm and Yarn setup pages (settings, units, defaults, exemptions, errors, no pnpm CLI flag or env var, Yarn quarantine of unreadable publish dates, npm audit fix). Fixed: npm default wording now matches the page (off, still in npm 12).
Method: documentation only; no commands were run.

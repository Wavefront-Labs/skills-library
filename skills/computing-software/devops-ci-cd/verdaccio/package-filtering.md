---
id: computing-software.devops-ci-cd.verdaccio.package-filtering
name: package-filtering
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [package-filter, quarantine, min-age-days, minagedays, datethreshold, block-allow, secfilter, supply-chain]
level: advanced
status: docs-checked
description: "Hide risky package versions with the bundled @verdaccio/package-filter (minAgeDays, dateThreshold, block, allow, replace strategy) or the secfilter plugin."
sources:
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/plugins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since 6.4.0 an optional bundled filter controls which versions appear in manifest responses. Disabled until listed under `filters`:

```yaml
filters:
  '@verdaccio/package-filter':
    minAgeDays: 7
    dateThreshold: '2025-01-01'
    block:
      - scope: '@malicious'
      - package: 'typosquat-pkg'
      - package: 'compromised-lib'
        versions: '>=3.0.0'
      - package: 'legacy-lib'
        versions: '>=2.0.0'
        strategy: replace
    allow:
      - scope: '@my-org'
      - package: 'compromised-lib'
        versions: '3.0.1'
```
- `minAgeDays`: hide versions published fewer than N days ago (quarantine).
- `dateThreshold`: serve only versions before the date; with `minAgeDays` the earlier cutoff wins.
- `block`: rules by scope, package, or package plus semver range; `strategy: replace` substitutes the nearest older safe version (good for transitive deps).
- `allow`: exempts matches from all rules, including age and date, and beats `block`.

Third-party option `verdaccio-plugin-secfilter` uses `filters: plugin-secfilter: block:` with `scope`, `package`, `versions` (semver syntax).

## Checked

2026-11-04. Confirmed against the Verdaccio Configuration page (package-filter since 6.4.0, minAgeDays, dateThreshold earlier-cutoff rule, block and strategy replace, allow precedence) and Plugins page (secfilter example). Removed: the closing Verify tip.
Method: documentation only; no commands were run.

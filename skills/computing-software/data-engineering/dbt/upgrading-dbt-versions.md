---
id: computing-software.data-engineering.dbt.upgrading-dbt-versions
name: upgrading-dbt-versions
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-upgrade, deprecations, behavior-flags, require-dbt-version, adapter-versions, dbt-fusion, release-tracks, package-compatibility]
level: advanced
status: gated
description: "Upgrade dbt Core/adapters safely: read migration guides, pin versions, handle deprecation warnings and behavior change flags, check package version ranges, and compare outputs."
sources:
  - https://docs.getdbt.com/docs/dbt-versions/core-upgrade
  - https://docs.getdbt.com/reference/global-configs/behavior-changes
  - https://docs.getdbt.com/reference/project-configs/require-dbt-version
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading dbt versions

**Goal:** move to a new dbt minor version (and adapter) without silent behaviour changes in production.

## 1. Read the migration guide
Each minor release has an "Upgrading to vX.Y" page listing breaking changes, new deprecations and behaviour flags. Read every version you skip.

## 2. Pin and upgrade together
```text
# requirements-dbt.txt
dbt-core==1.10.*
dbt-snowflake==1.10.*      # adapter minor should match core minor
```
```yaml
# dbt_project.yml
require-dbt-version: [">=1.10.0", "<1.11.0"]
```
Upgrade in a branch; run CI with the new versions.

## 3. Clear deprecations first
Run on the current version and fix warnings (`dbt parse --show-all-deprecations` in recent versions; or `--warn-error-options '{"error": ["Deprecations"]}'` to make them fail in CI). Examples across recent versions: `tests:` -> `data_tests:`, top-level test arguments -> `arguments:`, custom keys in YAML -> `meta`/`config`, snapshot SQL blocks -> YAML. (gated: unconfirmed, source is paywalled or blocked)

## 4. Behavior change flags
New behaviours ship behind flags defaulting to the old behaviour for a period:
```yaml
flags:
  require_explicit_package_overrides_for_builtin_materializations: true
  source_freshness_run_project_hooks: true
```
Turn each on deliberately, test, and document. When the flag's default flips in a later release, you're already compatible.

## 5. Packages
`packages.yml` version ranges must support the new dbt version (`require-dbt-version` inside packages). Upgrade dbt_utils etc. in the same branch: `dbt deps --upgrade` (1.7+ lock file `package-lock.yml`).

## 6. Compare outputs
Build key marts in a CI schema with the new version and diff against prod (row counts, sums per key column, or data-diff tools). Compiled SQL diffs (`target/compiled`) between versions catch macro behaviour changes.

## 7. dbt Cloud release tracks / Fusion
dbt Cloud uses release tracks (Latest/Compatible/Extended) instead of pinned versions; the dbt Fusion engine (Rust) has its own compatibility requirements: run its conformance checks before switching.

## Verify
- [ ] CI green with new versions and no deprecation warnings.
- [ ] Mart diffs show no unexpected changes.
- [ ] Rollback plan: previous requirements pinned in git, prod image tagged.

## Checked

2026-11-02

- Confirmed: The dbt behavior-changes page and the require-dbt-version page were fetched.
- Removed or gated: The core-upgrade page returned only a stub; deprecation flags (--show-all-deprecations, warn-error-options), the lock file claim and the example flag names are gated, confirm in the current upgrade guide.

Method: documentation only; no commands were run.

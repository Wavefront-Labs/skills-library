---
id: computing-software.software-engineering.pnpm.minimum-release-age
name: minimum-release-age
category: computing-software
field: software-engineering
product: pnpm
tags: [minimum-release-age, minimum-release-age-exclude, minimum-release-age-strict, minimum-release-age-prune, ignore-missing-time, trust-policy-exclude, trust-policy-ignore-after, trust-lockfile-setting]
level: practitioner
status: docs-checked
description: "Delay new releases with pnpm minimumReleaseAge: exclusions, strict mode, pruning, registries without a time field, and related trustPolicy exclude and trustLockfile."
sources:
  - https://pnpm.io/settings/dependency-resolution
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
minimumReleaseAge: 1440          # minutes, default 1440
minimumReleaseAgeExclude:
  - webpack
  - '@myorg/*'
  - nx@21.6.5
  - webpack@4.47.0 || 5.102.1
```

- Applies to all dependencies including transitive. It does not apply to a config dependency pinned with `version+integrity`.
- `minimumReleaseAgeExclude` matches by package name (all versions), by pattern, or by exact versions joined with `||`.
- `minimumReleaseAgeStrict`: when no version in range is old enough, `true` fails resolution, `false` falls back to a newer version. Default is true only if you set `minimumReleaseAge` explicitly; the built-in 1440 default is non-strict.
- `minimumReleaseAgeExcludePrune` (false): install, add, update, remove and dedupe drop exclude entries the new lockfile no longer resolves. Name patterns are kept. Skipped when `sharedWorkspaceLockfile: false`.
- `minimumReleaseAgeIgnoreMissingTime` (true): skip the check when registry metadata has no `time` field. Set `false` to fail instead. It also governs `trustPolicy: no-downgrade`, which otherwise would fail with `ERR_PNPM_MISSING_TIME`.

Trust policy companions: `trustPolicy: no-downgrade`, `trustPolicyExclude` (selectors such as `'chokidar@4.0.3'`), `trustPolicyIgnoreAfter` (minutes; older versions skip the check), `trustPolicyExcludePrune` (v12.4.0).

`trustLockfile` (false) skips re-verifying the lockfile against these policies. Leave it false when outsiders can edit the lockfile.

## Checked

2026-11-04. Confirmed against pnpm.io/settings/dependency-resolution: minimumReleaseAge default and scope, exclude forms, Strict default rule, ExcludePrune, IgnoreMissingTime and ERR_PNPM_MISSING_TIME, trustPolicy companions (v12.4.0 prune), trustLockfile. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.

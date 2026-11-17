---
id: computing-software.devops-ci-cd.github-actions.cache-lookup-only-and-fail-on-cache-miss
name: cache-lookup-only-and-fail-on-cache-miss
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, lookup-only, fail-on-cache-miss, cache-hit-output, cache-matched-key, cache-primary-key, skip-build-on-hit, warm-cache-job, cache-restore, cache-save, enablecrossosarchive, save-always, actions-cache, cache-gating]
level: practitioner
status: docs-checked
description: "Use actions/cache lookup-only to test for a hit without downloading, fail-on-cache-miss to make consumer jobs strict, and cache-hit/cache-matched-key outputs to skip rebuilds."
sources: ["https://github.com/actions/cache#inputs", "https://github.com/actions/cache/blob/main/restore/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lookup-only and fail-on-cache-miss

**Goal:** decide in seconds whether an expensive build can be skipped, and make downstream
jobs refuse to run on a cold cache instead of silently rebuilding.

## 1. Inputs and outputs
| input | effect |
|---|---|
| `lookup-only: true` | only checks that the cache entry exists and skips the download (default false); on the combined `actions/cache` action it does not change save behaviour |
| `fail-on-cache-miss: true` | step fails if neither `key` nor `restore-keys` match |
| `enableCrossOsArchive: true` | lets Windows runners save or restore caches that other platforms can also restore or save (default false) |

Outputs: `cache-hit` (`'true'` only for an **exact** `key` match; for a partial `restore-keys` match or a miss the
restore action sets `false`, and the combined action sets an empty string on a miss), `cache-primary-key` (the primary key
passed in) and `cache-matched-key` (the key of the cache that was restored: the primary key, or a partial or complete
match of a restore key). The last two are documented for the `actions/cache/restore` action.

## 2. Skip the build when the exact key exists
```yaml
- id: probe
  uses: actions/cache/restore@v5
  with:
    path: dist
    key: build-${{ runner.os }}-${{ hashFiles('src/**', 'package-lock.json') }}
    lookup-only: true
- if: steps.probe.outputs.cache-hit != 'true'
  run: npm ci && npm run build
- if: steps.probe.outputs.cache-hit != 'true'
  uses: actions/cache/save@v5
  with: { path: dist, key: "${{ steps.probe.outputs.cache-primary-key }}" }
```
`cache-hit` is a string: compare to `'true'`, not a boolean.

## 3. Strict consumers
```yaml
- uses: actions/cache/restore@v5
  with:
    path: dist
    key: build-${{ runner.os }}-${{ hashFiles('src/**', 'package-lock.json') }}
    fail-on-cache-miss: true
```
Use in jobs that `needs:` the builder: a miss means the key logic diverged between jobs
(different `hashFiles` globs, different `runner.os`) — better to fail loudly than to rebuild.
Consider omitting `restore-keys` when you need an exact match, and check `cache-hit` afterwards.

## 4. Warm-cache job on the default branch
```yaml
on:
  push: { branches: [main] }
  schedule: [{ cron: '23 2 * * *' }]
jobs:
  warm:
    steps:
      - uses: actions/cache@v6
        with: { path: ~/.npm, key: "npm-${{ hashFiles('**/package-lock.json') }}" }
      - run: npm ci
```
The default branch cache is available to other branches (caches are scoped to key, version and branch), so this
gives pull requests something to restore.

## 5. Gotchas
- `cache-hit` is a string: compare to `'true'`.
- Runs with read-only cache access (for example a pull request from a fork) can restore but not save; the save step
  warns and completes without writing an entry.
- Check the README of the current major (v6 at the time of review) before copying `@vN` tags.

## Verify
- [ ] Second run after a build shows `cache-hit: true` and skips the build step.
- [ ] Consumer job fails when the key is wrong.

## Checked

Date: 2026-10-25. Documentation release: actions/cache README (latest release v6.1.0).
- Inputs lookup-only, fail-on-cache-miss, enableCrossOsArchive and defaults; cache-hit semantics; cache-primary-key and cache-matched-key outputs on restore; cache scope (key, version, branch; default branch available to others); read-only cache runs: confirmed in the actions/cache README and restore/README (latest release v6.1.0; README examples use cache@v6, restore@v5).
- Removed unconfirmed claims: save-always deprecation, restore-keys satisfying fail-on-cache-miss, immutable-key log text, lookup-only gating pattern and error text.

Method: documentation only; no commands were run.

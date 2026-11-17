---
id: computing-software.qa-testing-engineering.playwright.merging-blob-reports-from-shards
name: merging-blob-reports-from-shards
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright, merge-reports, blob-reporter, playwright-sharding, playwright-reporters, github-actions, ci]
level: practitioner
status: docs-checked
description: "Shard Playwright across CI machines and merge per-shard blob reports into one HTML report with npx playwright merge-reports, including a GitHub Actions example."
sources:
  - https://playwright.dev/docs/test-sharding
  - https://playwright.dev/docs/test-reporters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharding and merging blob reports

**Goal:** split a long suite across machines and still get a single report.

## Sharding
```bash
npx playwright test --shard=1/4    # machine 1 of 4
```
With `fullyParallel: true`, sharding splits at test level (balanced); otherwise at file level (uneven if files differ in size).

## Blob reporter
```ts
reporter: process.env.CI ? 'blob' : 'html'
```
Each shard writes a zip into `blob-report/`, named `report-<hash>-<shard_number>.zip` when sharding is used, so names do not clash when merged.

## GitHub Actions
```yaml
jobs:
  test:
    strategy: { fail-fast: false, matrix: { shardIndex: [1,2,3,4], shardTotal: [4] } }
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with: { node-version: lts/* }
      - run: npm ci && npx playwright install --with-deps
      - run: npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with: { name: blob-report-${{ matrix.shardIndex }}, path: blob-report, retention-days: 1 }
  merge:
    if: ${{ !cancelled() }}
    needs: [test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with: { node-version: lts/* }
      - run: npm ci
      - uses: actions/download-artifact@v5
        with: { path: all-blob-reports, pattern: blob-report-*, merge-multiple: true }
      - run: npx playwright merge-reports --reporter html ./all-blob-reports
      - uses: actions/upload-artifact@v4
        with: { name: html-report, path: playwright-report, retention-days: 14 }
```
`merge-reports` accepts several reporters, for example `npx playwright merge-reports --reporter=html,github ./blob-reports`; when merging reports from different operating systems, pass an explicit `--config=merge.config.ts` so the tests root is unambiguous.

## Gotchas
- The docs' workflow sets `fail-fast: false` so all shards run, and runs the merge job with `if: ${{ !cancelled() }}` so it merges even when some shards failed.
- Sharding only works on tests that can run in parallel; by default that means files are the unit unless `fullyParallel` is set.

## Verify
The merged HTML report contains all tests from all shards with traces attached for failures.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: the --shard=x/y flag, test-level versus file-level balancing with and without fullyParallel, the blob reporter via process.env.CI ? blob : html, blob file naming, the GitHub Actions matrix workflow including fail-fast false, upload and download of blob-report-* artifacts with merge-multiple, merge-reports with --reporter html, several reporters and --config. Updated: action versions to match the docs workflow (checkout and setup-node v6, download-artifact v5, upload-artifact v4). Removed: the same-version claim.

Method: documentation only; no commands were run.

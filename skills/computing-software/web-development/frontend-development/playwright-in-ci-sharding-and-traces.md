---
id: computing-software.web-development.frontend-development.playwright-in-ci-sharding-and-traces
name: playwright-in-ci-sharding-and-traces
category: computing-software
field: web-development
product: frontend-development
tags: [playwright-sharding, playwright-trace, e2e-ci, github-actions, merge-reports, frontend-testing]
level: practitioner
status: docs-checked
description: "Running Playwright reliably in CI: container images, webServer config, retries with traces on first retry, sharding with blob reports and merge-reports, and triaging failures."
sources:
  - https://playwright.dev/docs/ci-intro
  - https://playwright.dev/docs/test-sharding
  - https://playwright.dev/docs/trace-viewer
  - https://playwright.dev/docs/docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playwright in CI: sharding and traces

## 1. Config for CI
```ts
// playwright.config.ts
export default defineConfig({
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? "50%" : undefined,
  reporter: process.env.CI ? [["blob"], ["github"]] : "html",
  use: { baseURL: process.env.BASE_URL ?? "http://localhost:4173",
         trace: "on-first-retry", screenshot: "only-on-failure", video: "retain-on-failure" },
  webServer: process.env.BASE_URL ? undefined : {
    command: "npm run build && npm run preview -- --port 4173",
    url: "http://localhost:4173", reuseExistingServer: !process.env.CI, timeout: 120_000 },
});
```
Run against a production build (`preview`), not the dev server: dev mode is slower and behaves differently.

## 2. GitHub Actions with shards
```yaml
jobs:
  e2e:
    runs-on: ubuntu-latest
    container: mcr.microsoft.com/playwright:v<version>-noble   # use the exact @playwright/test version you installed
    strategy: { fail-fast: false, matrix: { shard: [1, 2, 3, 4] } }
    steps:
      - uses: actions/checkout@v6
      - run: npm ci
      - run: npx playwright test --shard=${{ matrix.shard }}/4
      - uses: actions/upload-artifact@v5
        if: ${{ !cancelled() }}
        with: { name: blob-${{ matrix.shard }}, path: blob-report, retention-days: 7 }
  report:
    needs: e2e
    if: ${{ !cancelled() }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - run: npm ci
      - uses: actions/download-artifact@v5
        with: { path: all-blob-reports, pattern: blob-*, merge-multiple: true }
      - run: npx playwright merge-reports --reporter html ./all-blob-reports
      - uses: actions/upload-artifact@v5
        with: { name: playwright-report, path: playwright-report }
```
Without the container: `npx playwright install --with-deps chromium` (install only browsers you test).

## 3. Triage
- Download the report; open failed tests' traces: `npx playwright show-trace trace.zip` (or trace.playwright.dev). The trace has DOM snapshots per action, network, console and source.
- "Flaky" label = passed on retry: treat as a bug, not a pass. Track with the HTML report's flaky filter.
- Reproduce locally with the same browser and `--repeat-each=20 --workers=4` to surface races.

## Gotchas
- Shards split by file unless `fullyParallel: true`, which balances individual tests across shards.
- Screenshots differ between browsers and platforms (the snapshot name includes both); generate visual baselines in the same Docker image CI uses.
- Secrets for staging logins: use `storageState` produced by a setup project, not UI login in every test.

## Verify
- [ ] A deliberately failing test produces a merged HTML report artifact with a trace attached.

## Checked

Checked 2026-10-26 against the Playwright docs source (microsoft/playwright `docs/src`, main, last commit 2026-10-25, latest release tag v1.64.1): CI, sharding, reporters, Docker, trace viewer and TestConfig pages.

- Fixed: the container image tag was pinned to an old release; the docs use `v%%VERSION%%-noble` (the installed version). The workflow now uses the action versions shown in the current docs (`actions/checkout@v6`, `upload-artifact@v5`, `download-artifact@v5`).
- Confirmed: `forbidOnly`, `retries`, `workers: "50%"` (percentage of logical cores), `blob` reporter on CI, `github` reporter, `--shard=x/y`, `merge-reports --reporter html`, `if: ${{ !cancelled() }}`, `fullyParallel` shard balancing, `--with-deps`, `npx playwright show-trace`, trace.playwright.dev, `trace: "on-first-retry"`.

Method: documentation only; no commands were run.

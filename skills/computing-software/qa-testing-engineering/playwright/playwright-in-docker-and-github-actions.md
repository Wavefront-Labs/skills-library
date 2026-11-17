---
id: computing-software.qa-testing-engineering.playwright.playwright-in-docker-and-github-actions
name: playwright-in-docker-and-github-actions
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright, playwright-docker, playwright-github-actions, ci, docker, browsers-install]
level: practitioner
status: docs-checked
description: "Run Playwright in CI: official Docker image matching the package version, install-deps on runners, caching, artifacts for reports and traces, and container gotchas."
sources:
  - https://playwright.dev/docs/ci
  - https://playwright.dev/docs/docker
  - https://playwright.dev/docs/ci-intro
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playwright in Docker and GitHub Actions

**Goal:** a reproducible CI setup where browsers and OS dependencies match the Playwright version.

## GitHub Actions (runner install)
```yaml
- uses: actions/setup-node@v6
  with: { node-version: lts/*, cache: npm }
- run: npm ci
- run: npx playwright install --with-deps chromium     # only the browsers you use
- run: npx playwright test
- uses: actions/upload-artifact@v5
  if: ${{ !cancelled() }}
  with: { name: playwright-report, path: playwright-report/, retention-days: 30 }
```

## Docker image
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: mcr.microsoft.com/playwright:v<version>-noble   # match the @playwright/test version
      options: --user 1001
```
Tags: `:v<version>-noble` (Ubuntu 24.04), `:v<version>-jammy` (Ubuntu 22.04) and a newer Ubuntu variant are published; the docs recommend pinning to a specific version.
Locally, per the docs: `docker run -it --rm --ipc=host mcr.microsoft.com/playwright:v<version>-noble /bin/bash`.

## Container gotchas
- `--ipc=host` is recommended with Chromium; without it Chromium can run out of memory and crash.
- The image runs browsers as `root` by default, which disables the Chromium sandbox. That is fine for end-to-end tests of trusted code; for untrusted sites use `--user pwuser` with the documented seccomp profile.
- `--init` is recommended to avoid zombie processes (PID 1 handling).
- If the Playwright version in the image does not match the project's, Playwright cannot locate the browser executables.
- The docs recommend `workers: process.env.CI ? 1 : undefined` on CI for stability and reproducibility.

## Caching
The docs advise against caching browser binaries: restoring the cache takes about as long as downloading them, and on Linux the OS dependencies cannot be cached. Cache npm packages instead.

## Gotchas
- Screenshots differ between browsers and platforms, so baselines generated on macOS (`-darwin` files) do not match Linux CI; generate them in the same Docker image.

## Verify
CI log shows matching Playwright and browser versions; report and traces uploaded as artifacts on failure.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: the runner install flow (setup-node, npm ci, playwright install --with-deps, artifact upload with retention-days), the container job with image mcr.microsoft.com/playwright:v<version>-noble and options --user 1001, image tags, version-pinning advice, --ipc=host, --init, root versus pwuser and seccomp, the advice against caching browsers, and the workers recommendation for CI. Updated: action versions to match the docs workflow, and the image tag to a version placeholder. Removed: the quoted Executable-doesn't-exist error and the Firefox-root claim.

Method: documentation only; no commands were run.

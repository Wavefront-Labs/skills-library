---
id: computing-software.qa-testing-engineering.test-automation.ci-caching-for-test-speed
name: ci-caching-for-test-speed
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [ci-caching, dependency-cache, browser-cache, actions-cache, test-pipeline-speed]
level: practitioner
status: docs-checked
description: "Speed up CI test jobs with caching: package manager caches, Playwright/Cypress browser binaries, build outputs and test tool caches, with correct keys and invalidation."
sources:
  - https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/caching-dependencies-to-speed-up-workflows
  - https://playwright.dev/docs/ci#caching-browsers
  - https://docs.gitlab.com/ci/caching/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Caching dependencies and browsers to speed CI tests

## Package managers
```yaml
- uses: actions/setup-node@v4
  with: { node-version: 22, cache: npm }      # caches ~/.npm keyed on package-lock.json
- uses: actions/setup-python@v5
  with: { python-version: "3.12", cache: pip }
- uses: actions/setup-java@v4
  with: { distribution: temurin, java-version: 21, cache: maven }   # or gradle
```
Cache the **download cache**, not `node_modules` (keyed incorrectly it breaks; `npm ci` deletes it anyway).

## Browser binaries
Playwright docs do not recommend caching browser binaries: restore time is comparable to download time, and operating system dependencies (installed with `npx playwright install --with-deps`) are not cacheable. If you still cache them, key the cache on a hash of the Playwright version.
Alternatively use a container image with browsers preinstalled (`mcr.microsoft.com/playwright:v<version>-noble`), which avoids both download and cache.

## Tool caches
Test-tool caches (pytest, mypy, Jest, Gradle) and remote build caches can be cached the same way; check each tool's docs for its cache directory.

## Keys and invalidation
```yaml
key: deps-${{ runner.os }}-${{ hashFiles('**/package-lock.json') }}
restore-keys: deps-${{ runner.os }}-
```
Include OS, tool version and lockfile hash. Fallback `restore-keys` give partial hits.

## Gotchas
- GitHub removes cache entries not accessed for over 7 days and limits total cache size per repository: huge caches evict each other.
- Caches from PR branches aren't visible to other branches (scoped); main must populate them.
- Restoring a stale cache that "works" can hide lockfile drift; keys must include the lockfile hash.

## Verify
The cache step reports a hit; install step time drops on the second run.

## Checked
2026-10-28. Confirmed: Playwright CI page (caching browsers not recommended, key on Playwright version, `--with-deps`, `mcr.microsoft.com/playwright` image tags ending in `-noble`); GitHub dependency-caching page (`restore-keys`, key matching, branch scoping, 7-day eviction, total size limit). Removed: Playwright browser cache path and shell snippet, the Cypress cache claim, tool cache directory names, the 10 GB figure and the log message text.
Method: documentation only; no commands were run.

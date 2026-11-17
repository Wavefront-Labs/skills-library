---
id: computing-software.qa-testing-engineering.test-automation.smoke-and-sanity-suites
name: smoke-and-sanity-suites
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [smoke-testing, sanity-testing, regression-testing, build-verification-test, post-deploy-checks, synthetic-monitoring]
level: practitioner
status: docs-checked
description: "Build a smoke suite (build verification after every deploy) and use sanity checks for narrow post-fix verification; select them with test tags."
sources:
  - https://playwright.dev/docs/test-annotations
  - https://docs.pytest.org/en/stable/example/markers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Smoke and sanity suites

**Goal:** a fast, trustworthy "is this build worth testing / is production alive" signal.

## Smoke (build verification test)
- Broad and shallow: app starts, login works, each critical journey's first step responds, key integrations reachable, version endpoint shows the expected build.
- Runs after every deploy to every environment, including production (read-only or with synthetic test accounts).
- Keep it short and zero-tolerance for flakiness (a flaky smoke test gets fixed or removed promptly).

## Selecting the suite with tags
Playwright tags a test with a title token or a `tag` option (tags must start with `@`) and filters with `--grep`; `--grep-invert` excludes a tag:
```ts
test('checkout page loads', { tag: '@smoke' }, async ({ page }) => { /* ... */ });
// npx playwright test --grep @smoke
```
pytest selects by marker expression: mark tests with `@pytest.mark.<name>` and run `pytest -m <name>` (pytest markers can also be combined, for example `-m "interface or event"`, or negated with `not`). Register custom marker names in your pytest configuration to avoid unknown-marker warnings.

## Sanity
- Narrow and deeper: after a fix or a small change, check the affected function and its immediate neighbours before running full regression.
- Usually unscripted or a small selected set; record what was checked.

## Pipeline placement
deploy -> smoke (gate: fail = auto rollback or block promotion) -> broader regression.
Production smoke can double as synthetic monitoring if scheduled and wired to alerting.

## Gotchas
- Smoke tests that create data in production need cleanup and clearly marked test accounts.
- Checking only HTTP 200 on the home page misses broken JS bundles; assert visible key content.

## Verify
Deploy a deliberately broken build (e.g. bad config) to a test env: smoke fails within minutes and blocks promotion.

## Checked
2026-11-09. Confirmed in the Playwright Annotations page (tag option, @ prefix, --grep, --grep-invert) and the pytest markers example page (`pytest -m` marker expressions with or/not). Removed: the ISTQB source (the fetched page has no smoke or sanity definitions), JUnit Tag and Maven `-Dgroups` lines, the 5-minute budget and the 5-15 minute schedule (unsourced figures). The remaining process guidance is judgement, not a sourced claim.
Method: documentation only; no commands were run.

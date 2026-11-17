---
id: computing-software.qa-testing-engineering.playwright.only-changed-and-last-failed
name: only-changed-and-last-failed
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [only-changed, last-failed, playwright-cli, fast-feedback]
level: practitioner
status: docs-checked
description: "Shorten Playwright feedback loops with --only-changed (git-based test selection), --last-failed reruns, --grep, file:line filters and --list."
sources:
  - https://playwright.dev/docs/test-cli
  - https://playwright.dev/docs/running-tests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running only changed and last-failed tests

**Goal:** run the tests that matter for this change first.

## --last-failed
```bash
npx playwright test                 # full run, records failures in <outputDir>/.last-run.json
npx playwright test --last-failed   # rerun only those
```
`.last-run.json` lives in `outputDir` by default; `--last-failed-file <file>` (or `PLAYWRIGHT_LAST_RUN_OUTPUT_FILE`) overrides the path. A separate CI job needs that file carried over to use it.

## --only-changed
```bash
npx playwright test --only-changed            # vs HEAD: uncommitted changes
npx playwright test --only-changed=main       # vs a ref (PR checks)
```
Per the CLI reference: only run test files that have changed between `HEAD` and `ref`; with no ref it runs all uncommitted changes. Git only. The docs describe test files, so application source changes that a test exercises through the browser are not detected: treat it as a fast pre-check, not a replacement for the full suite.

PR pipeline pattern: run `--only-changed=<base ref>` first for a fast signal, then the full suite (or nightly). The base ref must exist in the checkout.

## Other filters
```bash
npx playwright test tests/cart.spec.ts:42      # test at line
npx playwright test -g "checkout" --grep-invert "@slow"
npx playwright test --project=chromium --list  # show what would run
npx playwright test --repeat-each=10 tests/flaky.spec.ts
```

## Gotchas
- A ref that is not present in the checkout (for example a shallow clone) cannot be compared; make sure it is fetched.
- Do not rely on `--only-changed` to pick up changes in helper or page-object files; confirm with `--list` before trusting it.

## Verify
Edit one spec file without committing; `npx playwright test --only-changed --list` lists that spec.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: the --last-failed flag, the default last-run file <outputDir>/.last-run.json and the --last-failed-file override, --only-changed [ref] semantics (test files changed between HEAD and ref, defaults to uncommitted changes, Git only), --list, --repeat-each, --project, --grep and --grep-invert, and the file:line filter. Removed: the claim that files importing changed modules are included, the fetch-depth and GITHUB_BASE_REF specifics, and the shallow-clone behaviour, which the docs do not state.

Method: documentation only; no commands were run.

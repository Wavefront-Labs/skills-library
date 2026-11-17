---
id: computing-software.qa-testing-engineering.test-automation.automated-accessibility-scans-axe-lighthouse
name: automated-accessibility-scans-axe-lighthouse
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [axe-core, lighthouse-accessibility, accessibility-testing, wcag, pa11y, ci-quality-gates]
level: practitioner
status: verified
description: "Automate accessibility scans with axe-core, pa11y-ci and Lighthouse in CI: rule tags, scoping, baselining known issues, and what automation cannot catch."
sources:
  - https://github.com/dequelabs/axe-core
  - https://github.com/pa11y/pa11y-ci
  - https://developer.chrome.com/docs/lighthouse/accessibility/scoring
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automated accessibility scans (axe-core, Lighthouse)

**Goal:** catch the machine-detectable WCAG failures on every build. Automated rules cannot find every issue (see "What automation misses"); manual keyboard and screen reader checks remain necessary.

## axe-core CLI / in tests
```bash
npx @axe-core/cli https://staging.example.test --tags wcag2a,wcag2aa,wcag21aa --exit
```
Run on axe-core 4.14.0 and @axe-core/cli with a local page containing an image without `alt` and an empty button: `--tags wcag2a,wcag2aa,wcag21aa --exit` reported `image-alt` and `button-name` and exited 1. Environment traps seen: the CLI's bundled chromedriver refuses a Chrome of a different major version ("This version of ChromeDriver only supports Chrome version 152", with Chrome 156 installed), so use `--chrome-path` to a matching browser or `npx browser-driver-manager install chrome`; and without `--load-delay 3000` one run scanned a blank `data:,` page and reported only `document-title` and `html-has-lang`, so add a load delay for pages that render after load.
In unit/component tests: `jest-axe` (`expect(await axe(container)).toHaveNoViolations()`; ran under vitest with jsdom: an image without `alt` gave violation id `image-alt` and a failing matcher, with `alt` it passed).
In E2E: `@axe-core/playwright` or `cypress-axe` (see the framework skills).

## pa11y-ci for many URLs
```json
// .pa11yci
{ "defaults": { "standard": "WCAG2AA", "runners": ["axe", "htmlcs"], "timeout": 30000 },
  "urls": ["https://staging.example.test/", "https://staging.example.test/checkout"] }
```
`npx pa11y-ci` exits non-zero on errors (pa11y-ci 5.0.0 exited 2 with 4 errors on the same page, reporting both axe and HTML_CodeSniffer findings; the file is named `.pa11yci`, plain JSON, so omit the `// .pa11yci` label line above, and add `chromeLaunchConfig.executablePath` to use an installed browser).

## Lighthouse CI
```bash
npx @lhci/cli autorun
```
```json
// lighthouserc.json
{ "ci": { "collect": { "url": ["https://staging.example.test/"], "settings": { "onlyCategories": ["accessibility"] } },
  "assert": { "assertions": { "categories:accessibility": ["error", { "minScore": 0.95 }] } } } }
```
Use a config file for assertions. With @lhci/cli 0.15.1 the command-line form `--assert.assertions.categories:accessibility='["error",{"minScore":0.5}]'` was ignored (the run still failed with `expected: >=0.9` from the default preset), while the same assertion in `lighthouserc.json` worked: minScore 0.5 passed (exit 0) and 0.95 failed (exit 1) on a page scoring 0.71.
The Lighthouse accessibility score is a weighted average of audits based on axe rules and impact (Lighthouse scoring docs); use it as a trend, gate on axe violations.

## Practical rules
- Scan each significant state (modal open, error shown, menu expanded), not just page load.
- Baseline known violations by rule id and selector with a ticket, fail only on new ones.
- Treat `serious` and `critical` impact as blocking.

## What automation misses
Meaningful alt text, logical focus order, keyboard traps in custom widgets, screen reader announcement quality, captions accuracy, cognitive load.

## Gotchas
- Colour contrast checks fail on gradients/images (reported as "needs review", not pass).
- Scans before content loads report nothing; wait for the page to settle.

## Verify
CI fails on a newly introduced violation (test by removing an `alt` or label), and the baseline list shrinks over time.

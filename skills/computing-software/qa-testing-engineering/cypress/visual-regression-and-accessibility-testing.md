---
id: computing-software.qa-testing-engineering.cypress.visual-regression-and-accessibility-testing
name: visual-regression-and-accessibility-testing
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress, visual-regression, visual-testing, screenshot-testing, percy, applitools, cypress-image-snapshot, axe, cypress-axe, accessibility, a11y, wcag, aria, color-contrast, diff-threshold, anti-aliasing, baseline, flaky-screenshots, ci]
level: practitioner
status: gated
description: "Add visual regression and automated accessibility checks to a Cypress suite: baseline images, diff thresholds that survive anti-aliasing noise, and cypress-axe scans gated in CI."
sources: ["https://github.com/dequelabs/axe-core", "https://docs.cypress.io/app/tooling/visual-testing", "https://www.deque.com/axe/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cypress: visual regression and accessibility checks

**Goal:** catch unintended pixel-level UI regressions and the most common WCAG
violations automatically, inside the same Cypress run, without drowning the suite
in noisy false failures.

## 1. Visual regression — two approaches
**Self-hosted diffing** (`cypress-image-snapshot`): free, but you own baseline storage and flakiness. Check compatibility first: its npm peer range is `cypress ^4.5.0`, it was last published in 2022, and with Cypress 16.2.0 its `support`/`plugin` setup failed at load with "`Cypress.env()` was removed in Cypress version 16.0.0 ... key being accessed was: `updateSnapshots`". On Cypress 16 pick a maintained plugin that supports it, or a hosted service.
```js
cy.get('[data-cy=dashboard]').matchImageSnapshot('dashboard', { failureThreshold: 0.02, failureThresholdType: 'percent' })   // API per the cypress-image-snapshot package; it does not load on Cypress 16 (see above)
```
**Hosted services** (for example Percy, `@percy/cypress`): rendering and diffing happen on the service, which adds a network dependency to every run. Per the `@percy/cypress` README: `import '@percy/cypress'` in the support file, then
```js
cy.visit('/dashboard'); cy.percySnapshot('dashboard')   // needs PERCY_TOKEN in the environment (gated: unconfirmed, source is paywalled or blocked)
```
Not run here: no Percy account or token. Exact masking options and pricing are vendor-specific; read the vendor docs.

## 2. The real failure mode: noisy baselines
Raw pixel diff fails on sub-pixel font rendering differences between a dev machine
and CI, and on anything date/time/random-data driven. Fixes, in order of value:
- Freeze the clock (`cy.clock()`) and seed any random data before snapshotting.
- Run visual tests only in the CI container (one OS/renderer), never compare
  local-captured baselines against CI-captured ones.
- Mask or exclude dynamic regions (ids, timestamps, ads, avatars) — every tool
  supports a region/selector ignore list; use it instead of raising the threshold,
  which hides real regressions too.
- Set a tolerance (`failureThreshold` in `cypress-image-snapshot`) above the anti-aliasing noise you measure on your own baselines but well under a real layout shift.
- Update baselines deliberately, reviewed in the PR diff (most CI visual tools post
  a baseline-approval UI) — never auto-accept on merge.

## 3. Accessibility scans with cypress-axe
```js
import 'cypress-axe'
cy.visit('/checkout')
cy.injectAxe()
cy.checkA11y(null, { rules: { 'color-contrast': { enabled: true } } }, null, false)  // 4th arg skipFailures: false (the default) fails the test on violations
```
`skipFailures: true` makes `checkA11y` pass regardless: with `true`, a test page with 6 violations (`label` critical, `document-title`, `frame-title`, `html-has-lang` serious, `landmark-one-main`, `region` moderate) still passed; with `false` it failed with "6 accessibility violations were detected". `cypress-axe@1.7.0` declares peer `cypress ^10 ... ^15`, so on Cypress 16 `npm i` needs `--legacy-peer-deps` (it worked in the 16.2.0 run). The second argument also accepts `includedImpacts: ['critical', 'serious']`, which a scoped run used.
Axe automates a subset of WCAG checks: missing alt text, bad ARIA roles,
contrast ratio failures, missing form labels, duplicate IDs, heading order. It
**cannot** catch what needs a human: keyboard-trap detection, meaningful focus
order, whether alt text is actually descriptive, or screen-reader announcement
quality — pair with a manual pass (see `exploratory-testing` for a manual a11y
charter).

## 4. Scoping and triage
Scan per route/component state, not just the landing page — a modal, an error
state and an empty state each have their own markup. Run `cy.checkA11y('[data-cy=modal]')`
scoped to the open modal so axe doesn't re-flag the whole page's known issues.
Triage violations by axe's `impact` field (`critical`/`serious`/`moderate`/`minor`);
gate CI on critical+serious only at first, expand once the backlog is cleared —
gating on everything day one usually gets the whole check disabled instead.

## 5. CI wiring
Both checks are slow relative to functional assertions — run them in a separate
CI job/tag (`cypress run --env grepTags=visual`) so a flaky screenshot diff
doesn't block the whole pipeline, and so they can be retried independently.

## Notes
Run on Cypress 16.2.0: `cypress-axe` 1.7.0 with `axe-core` 4.14 (`injectAxe`, `checkA11y` scoped to a selector, `includedImpacts`, violation callback), `cy.clock()`. The Percy call is gated as marked above. Check the installed cypress-axe version's signature before copying the `checkA11y` call verbatim.

## Verify
- [ ] Clock frozen and seeded data before every visual snapshot.
- [ ] Dynamic regions masked, not just a raised global threshold.
- [ ] Baseline updates go through PR review, never auto-merge.
- [ ] `cy.checkA11y` runs on every distinct UI state (empty, error, modal, loading).
- [ ] CI gate fails only on `critical`/`serious` axe violations to start.

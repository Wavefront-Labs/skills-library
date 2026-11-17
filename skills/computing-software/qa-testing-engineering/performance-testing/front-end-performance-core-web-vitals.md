---
id: computing-software.qa-testing-engineering.performance-testing.front-end-performance-core-web-vitals
name: front-end-performance-core-web-vitals
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [core-web-vitals, lighthouse-ci, front-end-performance, web-vitals, performance-budgets]
level: practitioner
status: docs-checked
description: "Test front-end performance: Core Web Vitals (LCP, INP, CLS) lab vs field, Lighthouse CI assertions in pipelines, and the web-vitals library for real-user monitoring."
sources:
  - https://web.dev/articles/vitals
  - https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/getting-started.md
  - https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md
  - https://github.com/GoogleChrome/web-vitals
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Front-end performance (Core Web Vitals, Lighthouse CI)

## The metrics (good thresholds at p75 of page loads)
- **LCP** Largest Contentful Paint <= 2.5 s (loading).
- **INP** Interaction to Next Paint <= 200 ms (responsiveness; became a stable Core Web Vital in 2024, retiring FID).
- **CLS** Cumulative Layout Shift <= 0.1 (visual stability).
Total Blocking Time (TBT) is lab-measurable and a proxy for INP, but is not itself a Core Web Vital.

## Lab vs field
- **Lab** (e.g. Lighthouse): good for testing features before release and catching regressions; tools that load pages without a user cannot measure INP, so use TBT as a proxy.
- **Field/RUM** (web-vitals library): real users, devices and networks; lab measurement is not a substitute for it.

## Lighthouse CI
```bash
npm install -g @lhci/cli
lhci autorun
```
```json
// lighthouserc.json
{ "ci": {
  "collect": { "url": ["https://example.com/"], "numberOfRuns": 3 },
  "assert": { "preset": "lighthouse:recommended" },
  "upload": { "target": "temporary-public-storage" }
} }
```
`numberOfRuns` sets how many times Lighthouse runs per URL. Assertions can check an audit's score (`minScore`), item count (`maxLength`) or numeric value (`maxNumericValue`), and the `assert` section fails the build when they are not met. Per-audit ids and resource-summary assertions are listed in the Lighthouse CI configuration page.

## RUM
```js
import { onLCP, onINP, onCLS } from 'web-vitals';
const send = (m) => navigator.sendBeacon('/rum', JSON.stringify(m));
onLCP(send); onINP(send); onCLS(send);
```
The web-vitals library also ships an attribution build that reports what caused a poor value; see its README.

## Gotchas
- Lighthouse CI defaults to the mobile strategy for PageSpeed Insights runs; check the settings you rely on.
- Measure the 75th percentile of page loads, segmented across mobile and desktop.

## Verify
LHCI fails the build when an assertion is missed, and RUM reports p75 LCP/INP/CLS.

## Checked
2026-11-01. Confirmed: thresholds, 75th percentile, INP/FID status, TBT as INP proxy and lab vs field wording (web.dev vitals article); `lhci autorun`, `temporary-public-storage`, `lighthouse:recommended` (Lighthouse CI getting started); `numberOfRuns`, `minScore`/`maxLength`/`maxNumericValue` (Lighthouse CI configuration); web-vitals imports and attribution build (README). Removed: Lighthouse audit-id assertions and byte budgets, WebPageTest, DevTools throttling figures, Lighthouse score variance claim, the `web-vitals/attribution` import path, and the field `rating` property.
Method: documentation only; no commands were run.

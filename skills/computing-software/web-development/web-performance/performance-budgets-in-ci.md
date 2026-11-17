---
id: computing-software.web-development.web-performance.performance-budgets-in-ci
name: performance-budgets-in-ci
category: computing-software
field: web-development
product: web-performance
tags: [performance-measurement, performance-budgets, lighthouse-ci, bundle-size, ci]
level: practitioner
status: docs-checked
description: "Enforcing performance budgets in CI: choosing metrics and thresholds, Lighthouse CI assertions, bundle size limits with size-limit, and handling noise and regressions."
sources:
  - https://web.dev/articles/performance-budgets-101
  - https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md
  - https://github.com/ai/size-limit
  - https://web.dev/articles/use-lighthouse-for-performance-budgets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Performance budgets in CI

## 1. Budget types
- **Quantity**: JS per route, CSS, images, number of requests, third-party bytes. The web.dev budgets article gives 170 KB of compressed/minified critical-path resources as an example starting point.
- **Milestone timings** (lab): LCP, TBT, CLS on a defined throttled profile.
- **Rule-based**: a Lighthouse score threshold.
Set from today's baseline (don't regress) and from competitive/target goals; tighten over time.

## 2. Bundle size (fast, deterministic - gate every PR)
```json
// package.json
"size-limit": [
  { "path": "dist/assets/index-*.js", "limit": "120 kB" },
  { "path": "dist/assets/vendor-*.js", "limit": "90 kB", "gzip": true }
]
```
`npx size-limit` in CI; the Size Limit GitHub action comments bundle size changes on PRs. Size Limit measures with Brotli by default; `"gzip": true` switches to Gzip. `bundlesize` is an alternative tool.

## 3. Lighthouse CI (timings and audits)
```js
// lighthouserc.js
module.exports = { ci: {
  collect: { url: ["http://localhost:3000/", "http://localhost:3000/product/1"], numberOfRuns: 3, startServerCommand: "npm run start" },
  assert: { assertions: {
    "largest-contentful-paint": ["error", { maxNumericValue: 2500, aggregationMethod: "median-run" }],
  } },
  upload: { target: "temporary-public-storage" },   // or an LHCI server for history
} };
```
`npx @lhci/cli autorun`.

## 4. Noise
Lab timings vary between runs: use several runs and the median (`numberOfRuns`, `aggregationMethod`), dedicated runners, fixed throttling. Gate hard on byte budgets; warn (not fail) on timings or use generous thresholds. Track field data (CrUX/RUM) separately - budgets in CI catch regressions, field data shows reality.

## 5. Process
Budget breach = discussion, not automatic block forever: either fix, or raise the budget with an explicit trade-off recorded in the PR.

## Checked
2026-10-31. Confirmed on the web.dev performance-budgets-101 article, the Lighthouse CI configuration doc and the Size Limit README: 170 KB critical-path example, `numberOfRuns`, `startServerCommand`, `temporary-public-storage`, `autorun`, Size Limit's Brotli default and `gzip` option, GitHub action comments. Removed: the 10-20% noise figure, TBT/CLS/resource-summary assertions and metric thresholds, Next.js and webpack alternatives.
Method: documentation only; no commands were run.

## Verify
A PR adding a large dependency fails the size check with a clear diff; LHCI reports are linked from the PR checks.

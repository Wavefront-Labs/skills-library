---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-hybrid-browser-protocol-tests
name: k6-hybrid-browser-protocol-tests
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [hybrid-load-test, k6-browser, web-vitals-load, browser-and-protocol]
level: practitioner
status: verified
description: "Combine k6 protocol-level load with a few k6 browser VUs in one test to measure front-end Web Vitals under backend load, with separate scenarios and thresholds."
sources:
  - https://grafana.com/docs/k6/latest/using-k6-browser/
  - https://grafana.com/docs/k6/latest/using-k6-browser/recommended-practices/hybrid-approach-to-performance/
  - https://grafana.com/docs/k6/latest/using-k6-browser/metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hybrid tests with browser Web Vitals and protocol load

**Idea:** generate the bulk of load cheaply at HTTP level, while a handful of real browsers measure what users experience (LCP, INP, CLS) under that load.

```js
import http from 'k6/http';
import { browser } from 'k6/browser';
import { check } from 'k6';

export const options = {
  scenarios: {
    load: { executor: 'constant-arrival-rate', rate: 200, timeUnit: '1s', duration: '10m', preAllocatedVUs: 200, exec: 'api' },
    ux: {
      executor: 'constant-vus', vus: 2, duration: '10m', exec: 'ui',
      options: { browser: { type: 'chromium' } },
    },
  },
  thresholds: {
    'http_req_duration{scenario:load}': ['p(95)<300'],
    'browser_web_vital_lcp': ['p(75)<2500'],
    'browser_web_vital_inp': ['p(75)<200'],
    'browser_web_vital_cls': ['p(75)<0.1'],
  },
};

export function api() { http.get(`${__ENV.BASE}/api/products`); }

export async function ui() {
  const page = await browser.newPage();
  try {
    await page.goto(`${__ENV.BASE}/products`);
    await page.locator('[data-test=product]').first().click();
    check(await page.locator('h1').textContent(), { 'title shown': (t) => !!t });
  } finally {
    await page.close();
  }
}
```

## Notes
- Browser VUs are far heavier than protocol VUs (the k6 docs warn of extra overhead per browser VU; I did not measure a per-VU figure, so the old "~1 core, hundreds of MB" number was removed). The docs suggest starting with 10% of VUs or fewer as browsers; keep them few and on generators with headroom.
- The k6 browser API is async and Playwright-like (`page.locator`, `waitForNavigation`).
- Web vitals are reported as `browser_web_vital_*` metrics (run on k6 2.3.0 with Chrome via `K6_BROWSER_EXECUTABLE_PATH`: `cls, fcp, inp, lcp, ttfb`; the old `fid` was removed in v2.0.0); also `browser_http_req_duration`, `browser_http_req_failed`, `browser_data_sent/received`. The example, scaled to 8 s against a local static site, ran with all four thresholds passing and `title shown` 11/11.
- Run headless (default); `K6_BROWSER_HEADLESS=false` locally to watch.

## Gotchas
- Mixing heavy browsers with high protocol load on one machine skews both; distribute or size up.
- INP needs interactions to mean anything: in the run above the click navigated to another page and `browser_web_vital_inp` was `0s`, so the `p(75)<200` threshold passed vacuously. Click something that stays on the page and check the reported value is non-zero.
- Browser traffic includes things you did not script: 11 of 33 `browser_http_req_failed` were favicon 404s on the local test server, so `browser_http_req_failed` can show failures that are not your pages.

## Verify
Summary shows both protocol and browser metrics; LCP degrades measurably when protocol load is raised.

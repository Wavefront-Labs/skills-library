---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-tags-and-groups
name: k6-tags-and-groups
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6-tags, k6-groups, k6, result-slicing, url-grouping]
level: practitioner
status: verified
description: "Slice k6 results with tags and groups: system tags, custom request and scenario tags, name tag for URL grouping, group() durations, and thresholds per tag."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/tags-and-groups/
  - https://grafana.com/docs/k6/latest/using-k6/k6-options/reference/#system-tags
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tags and groups for result slicing (k6)

## Tags on requests
```js
http.get(`${BASE}/api/products/${id}`, { tags: { name: 'GET /api/products/:id', type: 'catalog' } });
```
- The `name` tag replaces the URL in metrics, preventing one time series per product id (high cardinality).
- Or use the `http.url` template literal: ``http.get(http.url`${BASE}/api/products/${id}`)`` which sets `name` to the template.

## Test-wide and scenario tags
```js
export const options = {
  tags: { testid: 'checkout-2026-10-16', env: 'staging' },
  scenarios: {
    browse: { executor: 'constant-vus', vus: 50, duration: '10m', tags: { flow: 'browse' } },
    buy:    { executor: 'constant-arrival-rate', rate: 5, timeUnit: '1s', duration: '10m', preAllocatedVUs: 20, tags: { flow: 'buy' } },
  },
  thresholds: {
    'http_req_duration{flow:buy}': ['p(95)<800'],
    'http_req_duration{type:catalog}': ['p(95)<300'],
    'http_req_failed{flow:buy}': ['rate<0.005'],
  },
};
```
CLI: `k6 run --tag testid=run42 script.js`. A `testid` tag lets dashboards separate runs. Run on k6 2.3.0 with `options.tags.testid = 'checkout-x'` and `--tag testid=run42 --tag extra=1`: every point carried `testid=run42` (the CLI value wins) and `extra=1`; scenario tags (`flow`) and custom request tags (`type`) were present alongside.

## Groups
```js
import { group } from 'k6';
export default function () {
  group('01 browse', () => { http.get(`${BASE}/`); http.get(`${BASE}/api/products`); });
  group('02 checkout', () => { /* ... */ });
}
```
Requests inside get a `group` tag (`::01 browse`); `group_duration` metric measures the whole group. Nested groups create paths (run: `::01 browse::inner`, `::02 checkout::payment`) and `group_duration` is emitted for each level with the group path as its `group` tag.

## Dynamic tags
`exec.vu.tags.step = 'login'` and `exec.vu.metrics.tags.step = 'login'` (k6/execution) both worked on k6 2.3.0: following requests in that VU carried `step=login`. The tag stays set until you change it, so reset it at the end of the iteration.

## System tags
`status`, `method`, `url`, `name`, `group`, `check`, `scenario`, `expected_response`, `error_code`, `proto`, `tls_version`... Trim with `systemTags: ['status', 'method', 'name', 'group', 'scenario', 'check', 'expected_response']` to reduce output volume (run: points then carried only `expected_response, group, method, name, scenario, status`; `url` and `proto` were gone). The full default list is in the k6 options reference.

## Gotchas
- Groups inside async code/`Promise` chains do not work reliably; keep groups synchronous. The k6 docs say the metric context (tags, group) is only reliable in synchronous code; the opt-in `async-metric-context` feature flag propagates it across `await`.
- Too many unique tag values bloats Prometheus/InfluxDB outputs.

## Verify
Results can be filtered per flow and per endpoint name in the summary or dashboard, and thresholds exist for the business-critical slices.

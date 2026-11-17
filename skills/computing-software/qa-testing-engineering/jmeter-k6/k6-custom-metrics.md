---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-custom-metrics
name: k6-custom-metrics
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6-custom-metrics, k6, counter-gauge-rate-trend, k6-metrics, thresholds]
level: practitioner
status: verified
description: "Add k6 custom metrics (Counter, Gauge, Rate, Trend) for business timings and error rates, tag them, set thresholds on them, and read them in summaries and outputs."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/metrics/create-custom-metrics/
  - https://grafana.com/docs/k6/latest/javascript-api/k6-metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom metrics in k6 (Counter, Gauge, Rate, Trend)

## Types
| Type | Aggregation | Use for |
|---|---|---|
| `Counter` | sum, rate | business events (orders placed, retries) |
| `Gauge` | last, min, max | current values (queue depth read from API) |
| `Rate` | % of non-zero values | error/success ratios for a step |
| `Trend` | min, max, avg, med, p(90), p(95)... | custom timings (end-to-end checkout time, server-reported timings) |

## Example
```js
import http from 'k6/http';
import { check } from 'k6';
import { Counter, Rate, Trend } from 'k6/metrics';

const checkoutDuration = new Trend('checkout_duration', true);   // true = time values (ms display)
const checkoutFailed = new Rate('checkout_failed');
const ordersPlaced = new Counter('orders_placed');

export const options = {
  thresholds: {
    checkout_duration: ['p(95)<2000'],
    checkout_failed: ['rate<0.01'],
    'checkout_duration{payment:card}': ['p(95)<2500'],     // threshold on a tagged sub-metric
  },
};

export default function () {
  const start = Date.now();
  const basket = http.post(`${__ENV.BASE_URL}/api/basket`, '{"sku":"SKU-1"}');
  const pay = http.post(`${__ENV.BASE_URL}/api/pay`, '{"method":"card"}');
  const ok = check(pay, { 'paid': (r) => r.status === 201 });
  checkoutDuration.add(Date.now() - start, { payment: 'card' });
  checkoutFailed.add(!ok);
  if (ok) ordersPlaced.add(1);
}
```
Server timing header: `serverTime.add(Number(res.headers['Server-Timing'].match(/dur=(\d+)/)[1]))`.

## Notes
- Built-in `http_req_duration` excludes client-side processing; a Trend around several requests captures user-perceived flow time.
- Metric names: ASCII letters, digits and underscores only, starting with a letter or underscore (k6 rejects `bad-name`, `9bad` and `sp ace` with `Invalid metric name`; the registry regex is `^[a-zA-Z_][a-zA-Z0-9_]{1,128}$`); avoid high-cardinality tags (ids, URLs with ids) which explode outputs. Use `name` tag for grouped URLs (`http.get(url, { tags: { name: 'GET /products/:id' } })`).
- Include custom trends' percentiles in the summary: `summaryTrendStats: ['avg', 'p(90)', 'p(95)', 'p(99)', 'max']`.

## Gotchas
- Creating metrics inside VU code throws `metrics must be declared in the init context` (run); define them in init.
- A threshold on a sub-metric whose tag never occurs does not fail: `checkout_duration{payment:nope}` reported `p(95)=0s` and passed (k6 2.3.0, no warning).
- Trend with `isTime=false` (the default) prints raw numbers (`raw_numbers: avg=12.5`); pass `true` for durations so the summary shows time units (`avg=1ms`).

## Verify
Custom metrics appear in the end-of-test summary and outputs, and thresholds on them fail the run when violated.

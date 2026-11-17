---
id: computing-software.qa-testing-engineering.performance-testing.transaction-mix-and-journey-weighting
name: transaction-mix-and-journey-weighting
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [transaction-mix, journey-weighting, workload-mix, traffic-model]
level: practitioner
status: verified
description: "Build a load-test transaction mix from production data: journeys, per-endpoint rates, read/write ratios, weights in k6/JMeter/Locust and checking the achieved mix."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/
  - https://jmeter.apache.org/usermanual/component_reference.html#Throughput_Controller
  - https://docs.locust.io/en/stable/writing-a-locustfile.html#task-decorator
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transaction mix and journey weighting

## From data to mix
1. Pull a busy representative hour from access logs/APM: count requests per normalised endpoint (`/orders/{id}`).
2. Group endpoints into **journeys** (browse, search, add to cart, checkout, account) using session analytics.
3. Compute journeys per hour and each journey's share. Example: browse 60%, search 25%, checkout 10%, account 5%.
4. Keep the long tail honest: lump rare endpoints into an "other reads" task rather than dropping them, if together they exceed a few percent.
5. Separate background traffic (cron, webhooks, partner APIs) as its own scenario at its own rate.

## Implementing
k6, separate scenarios with their own rates (most explicit):
```js
export const options = {
scenarios: {
  browse:   { executor: 'constant-arrival-rate', rate: 60, timeUnit: '1s', duration: '30m', exec: 'browse',   preAllocatedVUs: 100 },
  search:   { executor: 'constant-arrival-rate', rate: 25, timeUnit: '1s', duration: '30m', exec: 'search',   preAllocatedVUs: 50 },
  checkout: { executor: 'constant-arrival-rate', rate: 10, timeUnit: '1s', duration: '30m', exec: 'checkout', preAllocatedVUs: 50 },
},
thresholds: {   // empty-bar thresholds just make k6 report per-scenario counts in the summary
  'http_reqs{scenario:browse}': ['count>=0'], 'http_reqs{scenario:search}': ['count>=0'], 'http_reqs{scenario:checkout}': ['count>=0'],
};
```
Each scenario needs `duration` (k6 refuses to start without it: "the duration is unspecified") and an exported function named by `exec`. A 4 s run of this config (rates 60/25/10 per second, 95 per second in total) logged 241 browse, 101 search and 41 checkout requests: 62.9% / 26.4% / 10.7% against the planned 63.2% / 26.3% / 10.5%, and about 96 requests/s in total (383 requests in 4 s).
Locust: task weights / User class weights (measured: weights 10:3:1 produced 235:72:25 requests). JMeter: separate Thread Groups with Precise Throughput Timers, or Throughput Controllers (set to percent executions or total executions) inside one group.

## Validate
After the run, compare achieved requests per endpoint with the model (tolerance ±5%). Journeys with errors terminate early and skew the mix: check that too.

## Gotchas
- A mix built from averages over 24 h misses peak-hour shape (e.g. checkout share rises at lunchtime).
- Cached vs uncached paths: hitting the same few products overstates cache hits; draw IDs from a realistic popularity distribution.
- Writes accumulate data; long tests change DB size and therefore performance.

## Verify
Achieved mix table (planned vs actual per journey and endpoint) is part of every results report.

## Checked
k6 v1.4.0 and Locust 2.47.0 on Windows against a local stdlib HTTP server.
- Run: the three-scenario k6 config with `exec` functions: without `duration` k6 rejects the config (quoted error); with `duration: '4s'` the per-scenario counts via `http_reqs{scenario:...}` sub-metrics in `--summary-export` JSON gave the shares in the body. Locust weighted tasks run (see the tasksets skill).
- Fetched: k6 scenarios page and JMeter component reference (Throughput Controller: percent executions and total executions; Precise Throughput Timer).

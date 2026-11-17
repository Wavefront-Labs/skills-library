---
id: computing-software.software-engineering.concurrency.load-testing-with-k6
name: load-testing-with-k6
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, benchmarking, load-testing, k6, gatling, open-model, arrival-rate, thresholds, stress-testing, soak-testing, performance-testing]
level: practitioner
status: draft
description: "Run meaningful load tests with k6 (or Gatling): open vs closed workload models, arrival-rate scenarios, thresholds as pass/fail SLOs, and load/stress/soak test types."
sources: ["https://grafana.com/docs/k6/latest/using-k6/scenarios/", "https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/", "https://grafana.com/docs/k6/latest/using-k6/thresholds/", "https://docs.gatling.io/reference/script/core/injection/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Load testing with k6

**Goal:** find out how the system behaves at expected and peak traffic before users do,
with results that reflect real latency.

## Open vs closed model (the most important choice)
- **Closed** (fixed virtual users looping): when the system slows, VUs send fewer
  requests, so the load generator politely backs off and hides latency (coordinated
  omission). Fine for "N concurrent users" questions.
- **Open** (fixed arrival rate): requests arrive at a set rate regardless of response
  time, like real internet traffic. Use for APIs and SLO validation.

## Script
```javascript
import http from "k6/http";
import { check } from "k6";

export const options = {
  scenarios: {
    api: {
      executor: "ramping-arrival-rate",       // open model
      startRate: 50, timeUnit: "1s",
      preAllocatedVUs: 200, maxVUs: 2000,
      stages: [
        { target: 500, duration: "5m" },      // ramp to expected peak
        { target: 500, duration: "15m" },     // hold
        { target: 1000, duration: "5m" },     // push past it
      ],
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<300", "p(99)<800"],
    dropped_iterations: ["count<100"],       // generator couldn't keep up -> raise maxVUs
  },
};

export default function () {
  const res = http.get(`${__ENV.BASE_URL}/api/products?page=1`, { tags: { name: "list" } });
  check(res, { "200": (r) => r.status === 200 });
}
```
`k6 run -e BASE_URL=https://staging.example.com script.js`; thresholds make the run
exit non-zero (CI gate).

## Test types
- **Load**: expected peak for 15-60 min; verify SLOs.
- **Stress**: ramp beyond peak until it breaks; learn the failure mode (graceful 429s or meltdown?).
- **Spike**: sudden jump (autoscaling, cold caches).
- **Soak**: hours at moderate load; leaks, connection exhaustion, disk growth.

## Making results valid
- Production-like environment and data volumes; warm caches deliberately or not, but know which.
- Realistic mix of endpoints and think times; use `tags` to break down per endpoint.
- The load generator must not be the bottleneck (watch its CPU; distribute or use k6 Cloud/k6-operator).
- Watch server-side USE/RED metrics during the test, not just client numbers.
- Gatling equivalent: `constantUsersPerSec` / `rampUsersPerSec` injection = open model.

## Verify
- [ ] Thresholds encode the SLO and fail the run when breached.
- [ ] `dropped_iterations` is ~0 (the intended rate was actually generated).

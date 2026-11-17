---
id: computing-software.qa-testing-engineering.jmeter-k6.load-test-scripts-and-ramp-profiles
name: load-test-scripts-and-ramp-profiles
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6, jmeter, apache-jmeter, locust, load-testing, performance-testing, stress-testing, soak-testing, spike-testing, ramp-up, stages, scenarios, executors, arrival-rate, open-model, closed-model, thresholds, think-time, correlation, percentiles, p95, p99, throughput, rps, non-gui-mode, html-dashboard, javascript, python]
level: practitioner
status: docs-checked
description: "Script and run load tests in k6, JMeter and Locust against systems you own: realistic scenarios, ramp/arrival-rate profiles, thresholds on p95 and errors, CLI runs and reading results."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/ramping-arrival-rate/
  - https://grafana.com/docs/k6/latest/using-k6/thresholds/
  - https://grafana.com/docs/k6/latest/using-k6/tags-and-groups/
  - https://jmeter.apache.org/usermanual/get-started.html#non_gui
  - https://docs.locust.io/en/stable/running-without-web-ui.html
  - https://docs.locust.io/en/stable/writing-a-locustfile.html
  - https://docs.locust.io/en/stable/running-distributed.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Load test scripts and ramp profiles: k6, JMeter, Locust

**Goal:** a repeatable load test against a test/staging environment you are
authorised to load, with a realistic traffic shape and pass/fail thresholds, whose
results you can trust. Workload design itself is covered in
computing-software.qa-testing-engineering.performance-testing.workload-modelling-and-bottleneck-analysis.

**Ground rule:** only load systems you own or have written permission to test, and
tell the people running shared infrastructure (CDN, WAF, third-party APIs) first —
a load test is indistinguishable from an attack to them.

## 1. k6 (JavaScript scripts, Go engine)
```js
// checkout.js  — run: k6 run checkout.js   (env: k6 run -e BASE_URL=<STAGING_URL> checkout.js)
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    shoppers: {
      executor: 'ramping-arrival-rate',   // open model: new iterations/s regardless of response time
      startRate: 5, timeUnit: '1s',
      preAllocatedVUs: 50, maxVUs: 300,
      stages: [
        { target: 50, duration: '5m' },   // ramp
        { target: 50, duration: '20m' },  // hold at target
        { target: 0,  duration: '2m' },   // ramp down
      ],
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],                       // <1% errors
    'http_req_duration{name:checkout}': ['p(95)<800'],    // p95 under 800 ms
  },
};
const BASE = __ENV.BASE_URL;
export default function () {
  const r = http.get(`${BASE}/api/products`, { tags: { name: 'products' } });
  check(r, { 'products 200': (x) => x.status === 200 });
  sleep(Math.random() * 3 + 2);                           // think time 2-5 s
  const c = http.post(`${BASE}/api/checkout`, JSON.stringify({ sku: 'A1', qty: 1 }),
    { headers: { 'Content-Type': 'application/json' }, tags: { name: 'checkout' } });
  check(c, { 'checkout 201': (x) => x.status === 201 });
}
```
A failed threshold makes the test finish with a failed status (k6 exits with code 99) — use that as the CI gate.
For dynamic URLs (`/orders/123`) use the `name` tag (URL grouping) so they do not create one metric series per URL. `ramping-vus` gives a closed model (fixed users) instead.

## 2. JMeter (GUI to build, CLI to run)
Build the plan in the GUI: Thread Group (threads, ramp-up, duration) › HTTP Request
samplers › HTTP Header Manager, CSV Data Set Config (test accounts/data),
Constant/Uniform Random Timer for think time, Response Assertion. For arrival-rate
loads, the Concurrency and Arrivals thread groups come from the `jpgc-casutg` plugin (Plugins Manager); newer JMeter also has a core, experimental Open Model Thread Group.
**Never load-test from the GUI** — listeners like View Results Tree eat memory and skew results:
```bash
jmeter -n -t plan.jmx -l results.jtl -e -o report/ -Jusers=200 -Jrampup=300
```
`-n` non-GUI, `-l` raw results, `-e -o` HTML dashboard (folder must not exist or be empty).
Read properties in the plan with `${__P(users,10)}`. Raise heap for big runs
(`HEAP` env var, default `-Xms1g -Xmx1g -XX:MaxMetaspaceSize=256m`, or `JVM_ARGS`).
**Correlation:** extract dynamic values (CSRF tokens, session/order IDs) with a
Regular Expression or JSON Extractor and reuse as `${var}` — a recorded script replaying
a stale token "passes" against an error page. Add assertions so that shows as a failure.

## 3. Locust (Python)
```python
from locust import HttpUser, task, between
class Shopper(HttpUser):
    wait_time = between(2, 5)
    @task(3)
    def browse(self): self.client.get("/api/products", name="products")
    @task(1)
    def checkout(self): self.client.post("/api/checkout", json={"sku": "A1", "qty": 1}, name="checkout")
```
```bash
locust -f shop.py --headless -u 300 -r 10 -t 25m -H <STAGING_URL> --csv out
```
`-u` users, `-r` spawn rate per second, `-t` run time, `-H` host. Scale out with `--master` / `--worker`. Users loop with `wait_time`; for rate-driven load use `constant_throughput`/`constant_pacing`/`poisson` wait times, or a custom `LoadTestShape` class for a custom load profile.

## 4. Running it so the numbers mean something
- **Watch the load generator.** If its CPU saturates or it runs out of ports/memory,
  you are measuring the generator. Run it close to (but not on) the system under test.
- Warm up first; exclude the ramp from steady-state statistics.
- Report **percentiles** (p50/p95/p99) and error rate per transaction — never the average alone.
- Compare throughput achieved vs. target: if latency rises while RPS plateaus below
  target, you have found saturation.
- Keep scripts, data files and the exact command in git so the run is repeatable.

## Verify
- [ ] Written permission / environment owner informed; target is not production unless agreed.
- [ ] Every request has a check/assertion on status *and* content.
- [ ] Dynamic values are correlated; no recorded tokens hard-coded.
- [ ] Thresholds on p95 and error rate make the run fail automatically.
- [ ] Generator CPU/memory monitored and stayed healthy during the run.

## Checked
Checked against the Grafana k6 docs sources (grafana/k6-docs, docs/sources/k6/next, last commit 2026-10-13, which document k6 v2) and the k6 Operator repository (grafana/k6-operator, last commit 2026-10-21). Also JMeter user manual sources and the Locust docs sources (locustio/locust, docs/, last commit 2026-10-24). Confirmed: `ramping-arrival-rate` options (startRate, timeUnit, preAllocatedVUs, maxVUs, stages), threshold syntax including the `http_req_failed` rate and `p(95)` forms, test fails on threshold breach (exit code 99), `-e` env option and `__ENV`, URL grouping with the `name` tag, JMeter `-n -t -l -e -o`, `${__P()}`, HEAP default, jpgc-casutg plugin, Locust `--headless -u -r -t -H --csv`, `--master`/`--worker`, wait_time options and LoadTestShape. The scripts themselves were not run.

Method: documentation only; no commands were run.

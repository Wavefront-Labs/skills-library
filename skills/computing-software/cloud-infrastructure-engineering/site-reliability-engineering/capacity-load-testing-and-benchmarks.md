---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.capacity-load-testing-and-benchmarks
name: capacity-load-testing-and-benchmarks
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [capacity-load-testing, capacity-benchmarks, load-testing, k6, per-instance-capacity, capacity-planning]
level: practitioner
status: docs-checked
description: "Establish per-instance service capacity at the latency SLO with a step-load test (k6 arrival-rate), so raw resources can be converted into QPS for the capacity plan."
sources: ["https://sre.google/sre-book/introduction/", "https://sre.google/workbook/managing-load/", "https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/ramping-arrival-rate/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Load testing to establish capacity

SRE Book (Introduction): mandatory steps in capacity planning are an accurate organic demand forecast that extends
beyond the lead time for acquiring capacity, an accurate incorporation of inorganic demand (launches, marketing
campaigns), and regular load testing of the system to correlate raw capacity (servers, disks) to service capacity.
Software slows as load is added, and a slowdown equates to a loss of capacity; SREs provision to meet a capacity
target at a specific response speed.

So you need a conversion factor: how much load one instance (pod, VM, shard) serves while meeting the latency
SLO. Re-measure it regularly, since software efficiency changes with releases.

## Method
1. Isolate one instance or a small fixed pool behind the real load balancer configuration, with production-like
   data and dependencies.
2. Use an **open model**: iterations start independently of how fast the system responds. In k6 the
   `ramping-arrival-rate` executor is open-model and varies the rate of iteration starts through `stages`.
3. Step the arrival rate up and hold each step long enough for the system to settle (your choice of duration).
4. Record throughput, latency percentiles, error rate and resource use at each step.
5. Capacity is the highest step that still meets the SLO with margin; stop at the knee.

## k6 ramping-arrival-rate
Documented options: `stages` (required, array of `target` and `duration`), `preAllocatedVUs` (required),
`startRate` (default 0), `timeUnit` (default 1s, constant across the scenario), `maxVUs` (default: same as
`preAllocatedVUs`). Do not put `sleep()` at the end of an iteration, since the executor already paces iterations
through the rate and `timeUnit`. If there are not enough allocated VUs, iterations cannot be started.
```javascript
import http from 'k6/http';
export const options = {
  scenarios: { steps: {
    executor: 'ramping-arrival-rate', startRate: 50, timeUnit: '1s',
    preAllocatedVUs: 200, maxVUs: 2000,
    stages: [
      { target: 100, duration: '1m' }, { target: 100, duration: '5m' },
      { target: 200, duration: '1m' }, { target: 200, duration: '5m' },
    ] } },
};
export default function () { http.get('https://service.example.com/api/search?q=test'); }
```
Extend the stages until the service passes its knee. Check pass or fail against your SLO from the recorded
results.

## Related capacity guidance (SRE Workbook, Managing Load)
- Keep the service far from key bottlenecks such as CPU and reserve enough spare capacity for both overload
  protection and redundancy; autoscalers need time to react when new instances cannot serve instantly.
- Set minimum and maximum scaling bounds so a bug (for example CPU burned without work) cannot deplete quota.
- Keep a minimum number of instances per location to hold spare capacity for failover.

## Gotchas
- Use a realistic request mix, not one endpoint.
- A saturated load generator looks like a saturated server; monitor the generator too.
- Keep autoscaling from changing the pool being measured.

## Verify
- [ ] Capacity-per-instance figure dated and tied to a release.
- [ ] Knee identified with latency and error graph attached.
- [ ] Plan uses the figure with target utilisation below the knee.

## Checked

Checked 2026-11-09. Confirmed against the SRE Book Introduction (capacity planning steps), the SRE Workbook Managing Load page (autoscaling guidance) and the k6 ramping-arrival-rate executor page (options, defaults, open model, no sleep). Removed: the p(99) and failure-rate threshold block, the k6 run command with environment variable, the 5-10 minute step hold, the 10 percent regression alert, the claim that closed models hide saturation, and CI benchmarking advice, none of which appeared on a page read.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.

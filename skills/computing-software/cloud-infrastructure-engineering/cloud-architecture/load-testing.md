---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.load-testing
name: load-testing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, scalability, load-testing, stress-testing, soak-testing, k6, locust, jmeter, gatling, azure-load-testing, distributed-load-testing, performance-testing]
level: practitioner
status: draft
description: "Plan and run load, stress and soak tests: workload model, test types, k6/Locust/managed generators, environment and data, provider policies, reading results."
sources: ["https://grafana.com/docs/k6/latest/testing-guides/test-types/", "https://learn.microsoft.com/azure/load-testing/overview-what-is-azure-load-testing", "https://aws.amazon.com/solutions/implementations/distributed-load-testing-on-aws/", "https://aws.amazon.com/ec2/testing/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Load and stress testing

## Test types (k6 terminology)
- **Smoke**: minimal load, verifies the script.
- **Average-load**: expected normal traffic — validates SLOs.
- **Stress**: above normal (e.g. 2× peak) — where does it degrade?
- **Spike**: sudden surge — does autoscaling keep up?
- **Soak**: hours at normal load — memory leaks, connection exhaustion, log/disk growth.
- **Breakpoint**: ramp until failure — find the capacity limit.

## Steps
1. **Workload model** from production: endpoint mix, think times, payload sizes, read/write ratio,
   user journeys. Unrealistic mixes produce meaningless results.
2. Environment: production-like sizing and data volume (DB with realistic row counts and indexes).
   Use isolated accounts; stub third parties or use their sandboxes with permission.
3. Tooling: k6 (JS scripts, thresholds as pass/fail), Locust (Python), Gatling, JMeter; managed
   distributed generators — Azure Load Testing, Distributed Load Testing on AWS, k6 Cloud.
4. Generate load from enough machines/regions that the **generator isn't the bottleneck**; monitor generator CPU.
5. Define pass criteria upfront: p95/p99 latency, error rate, throughput (k6 `thresholds`).
6. Observe the system: traces, DB metrics, saturation of each tier; find the first bottleneck.

```javascript
export const options = { stages: [{duration:'5m',target:500},{duration:'20m',target:500},{duration:'5m',target:0}],
  thresholds: { http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<300'] } };
```

## Gotchas
- Provider policies: most allow load testing your own resources but prohibit DDoS-like tests
  without approval; check AWS/Azure/GCP testing policies.
- CDN/WAF rate limits block generators — allow-list or test origin directly as well.
- Costs: large tests scale real infrastructure — budget them.

## Verify
- [ ] Results stored with the commit/version tested and compared to the previous run.

---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.capacity-planning
name: capacity-planning
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, capacity-planning, demand-forecasting, load-testing, headroom, utilisation-target, n-plus-one, n-plus-2, saturation, throughput, littles-law, queueing, bottleneck, service-quotas, limits, autoscaling, hpa, cluster-autoscaler, karpenter, predictive-scaling, peak-traffic, black-friday, launch-readiness, k6, locust, gatling, cost-per-request]
level: advanced
status: docs-checked
description: "Plan capacity for cloud services: forecast demand from business drivers, find per-instance limits by load testing, size for N+1 at peak with headroom, and track quotas."
sources: ["https://sre.google/sre-book/software-engineering-in-sre/", "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_manage_service_limits_monitor_manage_limits.html", "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_manage_service_limits_aware_quotas_and_constraints.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capacity planning — enough for the peak after a failure, not a lot more

**Goal:** know, for each service, how much load one unit can take, how much load is coming,
and the date you'll run out — early enough to fix it, including the parts autoscaling can't.

## 1. Why autoscaling doesn't remove the job
Autoscaling handles minute-to-minute variation. It does not handle: account/service **quotas**,
database write capacity, licences, IP space in subnets, provisioned throughput, upstream
rate limits, spot/instance-type availability in a zone, or cold-start lag during a spike.
Capacity planning is mostly about those.

## 2. Forecast demand
- Base on **business drivers**, not just extrapolated graphs: active users, orders/day,
  marketing events, launches, seasonal peaks (compare same week last year).
- Translate drivers to load: requests per user-session, writes per order, bytes per upload.
- Forecast **peak** load over your planning horizon, not the daily average. The SRE Book calls capacity planning a never-ending cycle: assumptions change, so revise the plan.

## 3. Find per-unit capacity by load testing
- Use k6, Locust, Gatling or replayed production traffic against a production-like stack.
- Ramp until the SLO breaks (latency threshold or error rate), not until the CPU hits 100% —
  the knee usually arrives earlier because of locks, connection pools, GC or a dependency.
- Record: max sustainable RPS per instance/pod at SLO, and the **bottleneck resource**.
- Little's law sanity check: concurrency = throughput × latency. 2,000 RPS at 150 ms needs ~300 in-flight requests — check pool and thread limits against it.
- Retest after major releases; capacity per instance silently regresses.

## 4. Size with headroom
Required units = forecast peak ÷ per-unit capacity at SLO, then:
- **N+1 (or N+2)** for failure: survive losing the largest failure domain (with 3 AZs, size so 2 can carry peak, i.e. 1.5x).
- **Growth/forecast error** headroom, chosen from your forecast confidence.
- **Target utilisation** below the knee found in load testing.
Example: 9,000 RPS peak, 600 RPS/pod at SLO → 15 pods; AZ loss across 3 AZs → 23; +20% growth → 28 pods.

## 5. Track the non-elastic limits
Maintain a table per service: limit, current usage at peak, % used, lead time to raise.
Examples: vCPU quota per region, DB max connections, IOPS/throughput, NAT/port allocations,
subnet free IPs, Kafka partitions, third-party API rate limits. The AWS Well-Architected Reliability Pillar says to
monitor quota usage against thresholds (including hard limits that cannot be raised), increase quotas ahead of
planned growth, never assume quotas will be increased automatically, and assess each Region's needs separately.
Request increases before the launch, not during it.

## 6. Events and launches
Launch readiness: forecast, load test above forecast, pre-scale (raise min replicas), confirm quotas, rehearse load shedding.

## Gotchas
- Averages hide peaks: a daily average of 1,000 RPS can mean 4,000 RPS at lunch.
- Load tests from one client region/IP hit different caches and rate limits than real users.
- Testing against a small database instance and extrapolating linearly is wrong — contention is non-linear.
- Retry storms multiply load during incidents; capacity for the peak must include retry amplification or have budgets/circuit breakers.
- Over-provisioning is also a failure (cost); revisit headroom quarterly with
  `computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.rightsizing-compute-workloads`.

## Verify
- [ ] Per-service per-unit capacity at SLO is measured and dated.
- [ ] Peak forecast for 3/6/12 months exists, tied to business drivers.
- [ ] Capacity at peak survives loss of the largest failure domain.
- [ ] Quota/limit table with usage and lead times; alerts before any limit is reached.
- [ ] Launches have a signed-off readiness checklist including a load test.

## Checked

2026-11-01. Confirmed against the SRE Book chapter Software Engineering in SRE (capacity planning as a
never-ending cycle; N + 2 redundancy as an intent example) and the AWS Well-Architected Reliability Pillar pages on
monitoring and managing quotas and on quotas and constraints. The sizing and Little's law figures are arithmetic.
Removed: the utilisation range, headroom percentage, 70% alert threshold, 2x load test and percentile figures, and the
unread Gunther citation.
Method: documentation only; no commands were run.

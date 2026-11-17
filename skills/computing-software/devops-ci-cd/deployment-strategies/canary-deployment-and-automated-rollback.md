---
id: computing-software.devops-ci-cd.deployment-strategies.canary-deployment-and-automated-rollback
name: canary-deployment-and-automated-rollback
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, canary, canary-release, canary-analysis, automated-canary-analysis, automated-rollback, auto-rollback, baseline, canary-vs-baseline, kayenta, spinnaker, argo-rollouts, flagger, golden-signals, error-rate, latency-p99, slo, burn-rate, sample-size, statistical-significance, mann-whitney, canary-cohort, traffic-splitting, progressive-delivery, abort-criteria]
level: advanced
status: draft
description: "Design canary analysis that catches bad releases and rolls back by itself: cohort choice, canary-vs-baseline comparison, metric selection, sample-size sanity, step timing and abort rules."
sources: ["https://sre.google/workbook/canarying-releases/", "https://netflixtechblog.com/automated-canary-analysis-at-netflix-with-kayenta-3260bc7acc69", "https://docs.flagger.app/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Canary deployment with automated rollback

**Goal:** a bad release is detected while it serves a small slice of traffic and is
withdrawn **without a human**, while good releases aren't blocked by noise.

Tool mechanics live elsewhere (Argo Rollouts:
`computing-software.devops-ci-cd.argo-cd.progressive-delivery-with-argo-rollouts`; Flagger,
Spinnaker/Kayenta, AWS CodeDeploy and App Mesh/ALB weights work similarly). This skill is
the analysis design those tools need.

## 1. Pick the cohort
- **Who:** start with low-blast-radius traffic — internal users/employees, one region or
  cell, free-tier accounts — then random percentage. Random alone is fine for stateless
  APIs with lots of traffic.
- **Stickiness:** route by a hash of user/session if mixed versions break a user's
  experience (UI assets, cache formats). Non-sticky canaries give better statistics but
  can show users both versions.
- **Non-HTTP workloads:** for queue consumers, canary = a subset of consumers (or a
  partition); for batch jobs, run the new version on a sample of inputs in shadow mode.

## 2. Compare against a baseline, not against history
Comparing canary to the big stable fleet is biased: the canary pods are fresh (cold
caches, JIT), fewer, and on different nodes. Netflix/Kayenta practice: deploy a
**baseline** — new pods running the *old* version, same count and age as the canary —
and compare canary vs baseline over the same window. Without a baseline, at least compare
canary vs stable over the *same time window*, never vs "last week".

## 3. Choose metrics
- **Must-have (abort on regression):** error rate (5xx, plus application-level failures
  that return 200), latency p99/p95, crash/restart count, saturation (CPU, memory growth —
  leaks show slowly).
- **Business guards:** checkout completion, login success, messages processed/s.
  These catch "returns 200 with empty body" bugs that technical metrics miss.
- Prefer **ratios** (errors/requests) over counts — canary traffic is small.
- Scope every query by version label (`role="canary"` vs `role="baseline"`); a query
  that silently returns fleet-wide values passes everything.

## 4. Is there enough data?
A step can only judge what it has seen. Rough sanity check: you want at least tens of
"bad events" expected under the failure you care about.
Example: fleet 200 req/s, canary 5% → 10 req/s → 6,000 requests in 10 min. To notice
error rate rising from 0.1% to 1%: baseline expects ~6 errors, regression ~60 —
detectable. At 0.5% weight or 2 a.m. traffic it isn't. Options: longer steps, larger
first weight, synthetic traffic, or "pass only with enough samples" (treat low volume as
*inconclusive* → pause for a human, not pass).
Statistical comparisons (Mann-Whitney U in Kayenta, per-metric) beat fixed thresholds
on noisy metrics like latency; fixed thresholds are fine for crashes and hard SLOs.
*Exact sample-size maths depends on your metric's variance — treat these numbers as a sanity check, not a design.*

## 5. Steps and timing
A common shape: 1% (catch crashes) → 5% → 25% → 50% → 100%, each 10-20 min of analysis.
- Make the first step long enough to cover startup-time problems and one full metric
  scrape+evaluation cycle (scrape interval × 3 at least).
- Slow-burn problems (memory leaks, hourly cron in-app, daily cache expiry) need a soak:
  keep the final pre-100% step longer, or keep baseline comparison running after promotion.
- Total time is a product decision: a 2-hour canary per deploy limits deploy frequency.

## 6. Automated rollback rules
- **Abort** = route all traffic back to stable and scale canary down. It must not need
  the CI system, Git or a human to be reachable.
- Fail on **N consecutive bad evaluations** (e.g. 2-3), not one blip — but a crashloop
  or error ratio > 5× baseline aborts immediately.
- After abort: mark the artifact as failed so automation doesn't retry it, notify the
  author with the failing metric + graph link, and require Git revert/fix to proceed.
- Exempt nothing silently: if analysis is skipped (metrics backend down), the safe
  behaviour is **pause**, not promote.
- Avoid flapping: no automatic re-promotion after an abort.

## 7. What canaries can't catch
Schema migrations already applied, data written in new formats, external side effects,
and problems that only show at 100% load (lock contention, quota limits). Pair with
expand/contract migrations and load tests.

## Verify
- [ ] Injecting a 2% error rate in a test build gets it aborted automatically at the first step.
- [ ] A known-good build passes 10 canaries in a row (false-abort rate measured).
- [ ] Queries are verified to return only canary/baseline series (check with a broken label).
- [ ] Metrics-backend outage during analysis results in pause, not promote.
- [ ] Abort works with CI and Git unreachable.

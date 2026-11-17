---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.cascading-failure-immediate-steps
name: cascading-failure-immediate-steps
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [cascade-immediate-steps, drop-traffic-recovery, cascading-failures, incident-response, load-shedding, mitigation]
level: advanced
status: docs-checked
description: "Stop a cascading failure in progress: add resources, stop health-check deaths, restart wisely, drop traffic and ramp back, enter degraded modes, kill batch load and bad traffic."
sources: ["https://sre.google/sre-book/addressing-cascading-failures/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Immediate steps to address a cascading failure

From the SRE Book section "Immediate Steps to Address Cascading Failures". In a cascade, normal
mitigations (rollback, scale) may not be enough because the system cannot recover at current load.

## Steps, roughly in order
1. **Increase resources**: add capacity if degraded capacity is the cause. Often insufficient alone once
   the cascade is under way (new tasks get overwhelmed immediately).
2. **Stop health check failures/deaths**: if health checks are killing tasks (liveness restarts, LB
   removal), disable or relax them temporarily so capacity stops shrinking.
   Prefer a pre-built runtime flag to make liveness always pass; editing the pod spec restarts pods.
   The book distinguishes process health checking (relevant to the cluster scheduler) from service health
   checking (relevant to the load balancer); keep them separate.
3. **Restart servers** if they are wedged (GC death spiral, in-flight requests without deadlines, deadlocks).
   Identify the source of the cascade first, canary the change and go slowly: restarting can amplify a cold-cache outage.
4. **Drop traffic**: a big hammer for a true cascade. If the whole service is crash-looping, the book suggests
   allowing only about 1% of traffic through, letting most servers become healthy, then ramping load up
   gradually so caches warm and connections establish. Drop less important traffic (e.g. prefetching) first.
   Fix or paper over the trigger first, or the cascade returns when traffic does.
5. **Enter degraded modes** (see `degraded-mode-design`): reduce work per request.
6. **Eliminate batch load**: pause batch jobs, backfills, indexing, crawlers that compete for capacity.
7. **Eliminate bad traffic**: block queries/clients that are causing heavy load or crashes (query of
   death); rate limit or WAF-block abusive clients.

## Drop-traffic ramp
Illustrative only (the steps and timings are not from the book): start very low at the LB or edge, hold each
step until saturation metrics are stable, step back on any regression, re-enable batch load last.

## Gotchas
- Undo temporary changes (health checks disabled, batch paused) and record each in the incident doc.
- Clients with aggressive retries will re-overload during ramp; shed retries at the edge if possible.
- Find the trigger before declaring resolved; otherwise it returns.

## Checked

2026-11-01. Confirmed against the SRE Book chapter Addressing Cascading Failures, section Immediate Steps (all
seven steps, the health-check distinction, the restart conditions, the 1% example and gradual ramp).
Removed: the 1-10% range, the CPU 70% check and the timed ramp table and the kubectl example (not in the book).
Method: documentation only; no commands were run.

## Verify
- [ ] Runbook includes the drop-traffic procedure with the exact commands/flags for your edge.
- [ ] Drill of the ramp procedure in a game day.

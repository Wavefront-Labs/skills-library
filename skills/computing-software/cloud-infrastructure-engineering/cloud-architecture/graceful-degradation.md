---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.graceful-degradation
name: graceful-degradation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, graceful-degradation, load-shedding, soft-dependencies, request-prioritisation, overload, brownout]
level: advanced
status: docs-checked
description: "Keep core functions up under dependency failure or overload: degraded modes, load shedding, request prioritisation, deadlines and testing past the goodput plateau."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_mitigate_interaction_failure_graceful_degradation.html", "https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/", "https://sre.google/sre-book/handling-overload/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Graceful degradation and load shedding

## Degraded modes (failure of a dependency)
1. Identify the core function and every dependency. Per AWS REL05-BP01, components should keep doing their core function
   when dependencies fail, perhaps serving stale data, alternate data or none; treat failure modes as normal operation.
2. Decide per dependency what to deliver. AWS examples: show the rest of an ecommerce landing page when one upstream
   system (recommendations) fails; continue a batch when one operation fails and report or dead-letter the failures;
   use the saga pattern to keep transactions consistent; use a circuit breaker for time-critical systems or a
   downstream under load; bake default parameters into images for an unavailable parameter store.
3. Treat it as a business decision, such as consistency versus availability, depending on the system.
4. Keep failure paths significantly simpler than the primary path and test them; AWS says fallback strategies
   should generally be avoided.
5. Do not drop monitoring silently: still run business functions if telemetry cannot be sent, but long silent gaps and
   missing compliance audit entries are not acceptable.

## Load shedding (overload)
1. Shed early: when a server nears overload it rejects excess requests so latency stays low for those it accepts and
   goodput holds (Amazon Builders' Library). Measure client-perceived availability and latency as well as server-side.
2. **Prioritise**: a load balancer ping is the most important request, since failing it idles the server; beyond that
   prioritisation varies by service (human requests over crawlers; `end()` calls over `start()`; later pagination
   pages over first pages). Conflicting heuristics across services can hurt systemwide availability.
   Google SRE assigns four criticality levels to requests (CRITICAL_PLUS, CRITICAL, SHEDDABLE_PLUS, SHEDDABLE)
   and propagates criticality across downstream calls.
3. **Deadlines**: use client timeout hints, propagate the remaining time across hops, and drop doomed requests.
4. **Bounded work**: paginate APIs so per-request load is estimable.
5. **Client-side throttling**: Google describes adaptive throttling based on the last two minutes of attempts, with
   backends ending up rejecting about one request per request processed in large overloads.
6. Instrument rejections (client, operation) and alarm on significant shedding; add capacity to address the bottleneck.

## Gotchas
- Retries multiply load: a timed-out client retries, turning one request into many.
- Load shedding can disable reactive autoscaling if both act on a similar CPU target.
- Dropping a request must be cheap; stray logging or socket settings can make it expensive.
- Untested degraded modes fail when needed.

## Verify
- [ ] Load test far beyond the goodput plateau: goodput stays steady as offered load rises.
- [ ] Each degraded mode and dependency failure path has been exercised.

## Checked
2026-11-08. Confirmed against AWS REL05-BP01, the Amazon Builders' Library "Using load shedding to avoid overload"
(shedding goal, goodput, prioritisation, deadlines, bounded work, autoscaling interaction, cost of dropping) and the
Google SRE book "Handling Overload" (adaptive throttling, four criticality values, propagation). Removed: kill
switches, HTTP 429/503 advice, Envoy and Netflix concurrency-limit libraries, retry-budget and 2x-capacity test
figure, game-day claim and the gateway priority header (not stated on these pages).
Method: documentation only; no commands were run.

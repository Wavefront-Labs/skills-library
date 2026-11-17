---
id: computing-software.cloud-infrastructure-engineering.aws.dependency-isolation-bulkheads-and-circuit-breakers
name: dependency-isolation-bulkheads-and-circuit-breakers
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, reliability, bulkhead, circuit-breaker, dependency-isolation, timeouts, retries, well-architected]
level: practitioner
status: gated
description: "Stop one failing dependency from taking down a service: timeouts, bounded retries with jitter, circuit breakers, bulkheads via concurrency and pools, load shedding."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_mitigate_interaction_failure_graceful_degradation.html", "https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/", "https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependency isolation: bulkheads, circuit breakers, timeouts

**Failure pattern:** a slow downstream (DB, partner API) ties up every thread/connection;
latency spreads upstream; retries multiply load; everything is down though only one
dependency is sick.

## 1. Timeouts on every call
- Set connect and request timeouts explicitly in every client, including AWS SDK clients.
- Timeout < caller's timeout (Lambda function timeout, API Gateway integration timeout, ALB idle timeout) so you can respond with a fallback.

## 2. Retries that don't amplify
- Retry only idempotent/transient failures, with **exponential backoff + jitter**, capped
  attempts; retry at one layer only (not client + service + SDK layers multiplying attempts).
- Token-bucket retry budgets (the AWS SDKs throttle retries with a token bucket, per the Builders' Library).

## 3. Circuit breaker
After N failures/timeouts in a window, fail fast for a cool-down, then let a probe through.
Implement in-process with a resilience library or at a proxy/mesh layer. Return a fallback (cached data, default, 503)
while open.

## 4. Bulkheads on AWS
- **Separate pools per dependency**: distinct HTTP connection pools/thread pools so the partner
  API can't consume DB capacity.
- **Lambda reserved concurrency** per function (one runaway consumer can't starve others) (gated: unconfirmed, source is paywalled or blocked);
  separate functions per dependency path.
- **SQS queues per work type/tenant** with their own consumers instead of one shared queue (gated: unconfirmed, source is paywalled or blocked).
- **Separate ECS services/target groups** for critical vs batch endpoints; ALB rules route them.
- **Cells/shuffle sharding** for multi-tenant isolation at larger scale.

## 5. Load shedding
Reject early when saturated (queue depth or in-flight count above a threshold → 503) rather
than accept work you'll time out on.

## Gotchas
- Fallbacks must be tested; an untested fallback is a second outage.
- Health checks that call dependencies (deep health checks) can take a whole fleet out of an
  ALB when one dependency fails — keep LB health checks shallow.

## Verify
- [ ] FIS/latency injection on one dependency: other endpoints keep their SLO; affected endpoint fails fast with fallback.
- [ ] Every outbound client has explicit timeouts and capped retries (code review checklist).
- [ ] Reserved concurrency/pool sizes documented per dependency.

## Checked

2026-10-28

Confirmed: circuit breaker pattern and graceful degradation (Well-Architected reliability page); exponential backoff with jitter, capped retries, retry at one layer, SDK retry token bucket (Builders' Library timeouts article); load shedding concept (Builders' Library).

Removed: boto3 Config values, API Gateway 29 s figure, 27x figure, Retry-After header, named libraries and mesh features, fair queues, edge throttling sentence.

Gated: Lambda reserved concurrency and SQS per-work-type queue bullets were not checked against the Lambda/SQS guides (not in this batch's pages); both are kept with the marker.

Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.cascading-failures-and-retry-budgets
name: cascading-failures-and-retry-budgets
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, cascading-failures, cascading-failure, retry-budget, retry-storm, retry-amplification, exponential-backoff, jitter, deadline-propagation, timeouts, bimodal-latency, cold-cache, slow-start, resource-exhaustion, server-overload, immediate-mitigations]
level: advanced
status: docs-checked
description: "Prevent and stop cascading failures per the SRE Book: overload mechanisms, retries with backoff, jitter and a retry budget, deadline propagation, bimodal latency, cold caches."
sources: ["https://sre.google/sre-book/addressing-cascading-failures/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cascading failures and retry budgets

**Goal:** a partial failure stays partial. All points below come from the SRE Book chapter Addressing
Cascading Failures.

## Mechanism
- One cluster failing sends its load to the others; they run out of resources, crash or miss deadlines, and
  successfully handled requests drop below what they could serve.
- Resource exhaustion shows up as long queues, thread starvation, file-descriptor exhaustion, CPU or memory
  pressure (Java GC death spiral), and health checks failing from starvation.
- A crash-looping fleet is hard to escape: dropping load slightly below the failure point will not stop the
  crashes, because capacity has shrunk; load must fall far enough for the few healthy tasks to cope.
- Load balancing policies that avoid servers that served errors can worsen it.

## Retries
Naive retries destabilise: backend load grows as retries add to it, and a meltdown redistributes requests onto
survivors. When retrying automatically:
- Use **randomized exponential backoff**; without randomness a small blip causes retry ripples that align and
  amplify.
- **Limit retries per request**; never retry indefinitely.
- Consider a **server-wide retry budget** (the book's example: allow 60 retries per minute in a process, then
  fail the request instead of retrying) so a capacity failure does not become a global cascade.
- Apply the overload protections below; graceful degradation reduces retry impact.
- To dig out, you may need to drastically cut or eliminate frontend load until retries stop.

## Deadlines
- Set a deadline: none, or an extremely high one, lets long-dead problems keep consuming resources. Very high
  deadlines drain higher layers; very short ones make costly requests fail consistently.
- Servers spend resources on requests that already exceeded the client deadline. Check the remaining deadline
  before each stage of work; exceptions exist, such as expensive catch-up with periodic checkpoints.
- **Propagate deadlines** instead of inventing new ones per hop; consider shaving a few hundred milliseconds
  for network transit and post-processing, and cap outgoing deadlines for noncritical backends, understanding
  your traffic mix.
- **Propagate cancellations** too (including when hedged requests complete) so doomed work stops.
- **Bimodal latency**: if a small fraction of requests never complete and the deadline is orders of magnitude
  above mean latency, they eat the thread pool and most requests fail. Look at latency distributions, not only
  means; fail fast on unavailable backends; consider limiting in-flight requests per client or keyspace.

## Slow start and cold caches
- Fresh processes are slower (connection setup, JIT, class loading) and cold caches make misses expensive.
  New or returned clusters and restarts all produce cold caches.
- A latency cache lets the service sustain expected load when empty; a capacity cache does not. Prefer the
  former, or overprovision, reject when overloaded, test large restarts, and raise load on a cluster slowly.
- Keep clusters carrying nominal load so caches stay warm; a separate cache binary can share caches across
  servers at the cost of an extra RPC.

## Preventing server overload (priority order in the chapter)
1. Load test capacity limits and the overload failure mode.
2. Serve degraded results.
3. Make servers reject requests when overloaded (fail early and cheaply).
4. Reject at higher levels (reverse proxies, load balancers, individual tasks); rate limiting that ignores
   service health may not stop a failure already under way.
5. Capacity planning coupled with performance testing (the book's example sizes a service to run at N + 2).

## Other triggers and structure
- Avoid intra-layer calls in the request path (distributed deadlock, load spikes); have the client retry on the
  correct backend instead of proxying.
- Triggers include process death (query of death), simultaneous updates (push off-peak or throttle in-flight
  updates), new rollouts (check recent changes and consider reverting; keep change logging), organic growth,
  drains, request profile changes, and reliance on slack CPU.

## Checked
2026-11-01. Confirmed against the SRE Book chapter Addressing Cascading Failures (read in full for the sections
above). Removed: Envoy, gRPC and Resilience4j configuration snippets, the multiplicative-amplification formula,
a 10 percent budget figure, health-probe and mitigation-order advice, and verify targets, none stated by the
fetched page.
Method: documentation only; no commands were run.

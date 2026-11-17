---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.backpressure-design
name: backpressure-design
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, distributed-systems-design, backpressure-design, backpressure, bounded-queues, admission-control, flow-control, client-side-throttling]
level: advanced
status: docs-checked
description: "Design backpressure so overload propagates upstream instead of collapsing services: bounded queues, load shedding, adaptive concurrency limits and client-side throttling."
sources: ["https://sre.google/sre-book/handling-overload/", "https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/", "https://github.com/Netflix/concurrency-limits"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backpressure and client-side throttling

## Mechanisms
- **Bounded waiting** (AWS Builders' Library): requests pile up in in-memory queues and TCP socket
  buffers. Cap how long a request may wait and discard requests that are too old. Spillover
  (fast-fail) is generally safer than surge queues.
- **Load shedding**: as a server approaches overload it rejects excess requests so those it accepts
  still finish quickly. Shedding has its own cost, so goodput eventually drops.
- **Prioritise what is shed**: examples from the Builders' Library are load balancer pings first,
  then (for example) `end()` calls above `start()` calls, later pagination pages above first pages,
  human traffic above crawlers. Google SRE uses four criticalities (`CRITICAL_PLUS`, `CRITICAL`,
  `SHEDDABLE_PLUS`, `SHEDDABLE`) that propagate to downstream calls; lower ones are rejected first.
- **Per-customer quotas** (Google SRE): set from negotiated usage, may sum to more than capacity;
  an over-quota customer gets errors while others are unaffected.
- **Client-side adaptive throttling** (Google SRE): each client tracks `requests` and `accepts` over
  the last two minutes; once requests exceed K times accepts it rejects new requests locally with a
  probability that rises with the gap. The book prefers K = 2; a lower K (e.g. 1.1) throttles more
  aggressively. (The formula is an image on the page and is not reproduced here.)
- **Adaptive concurrency limits** (Netflix concurrency-limits, Java): limit concurrent requests,
  not RPS, using Little's Law and a TCP congestion-window analogy. Vegas estimates queueing from
  minimum versus sampled RTT and moves the limit by 1; Gradient2 compares short and long latency
  averages and cuts sharply when divergence persists. Excess requests are rejected or callers blocked.

## Steps
1. Find every queue and buffer in the request path and bound its wait.
2. Choose what happens when full: reject, shed lowest priority first.
3. Retry carefully (Google SRE): stop a request after three attempts; allow a client to retry only
   while retries are under 10 percent of its requests; only the layer directly above a rejecting
   layer retries, to avoid combinatorial retry explosion; a backend can answer "overloaded; do not
   retry" when much of a datacentre is overloaded.
4. Propagate deadlines (Builders' Library): servers pass remaining time across hops and drop
   requests that can no longer succeed.
5. Load test well beyond capacity: goodput should plateau near full utilisation; if availability
   falls rapidly to zero, add shedding.

## Gotchas
- Work done for a client that has already timed out is wasted work.
- Retries at each layer of a deep call graph amplify load exponentially.

## Verify
- [ ] Offered load beyond capacity leaves goodput flat, not collapsing.

## Checked
Confirmed against the three cited pages (builder.aws.com is where the Builders' Library URL now
redirects). Removed because not stated there: HTTP 429/503 with Retry-After, Envoy adaptive
concurrency, reactive streams/gRPC/Kafka flow control, the written throttling formula (an image in
the SRE book), the "2x capacity" figure, AIMD detail (named only as a loss-based gRPC option).
Method: docs-only read of cited pages, 2026-11-08

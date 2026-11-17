---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.chatty-io
name: chatty-io
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, design-patterns-cloud, chatty-io, performance-antipatterns, n-plus-one, batching, round-trips]
level: practitioner
status: docs-checked
description: "Detect and fix the chatty I/O antipattern: many small requests to databases, APIs or files, found by load testing and telemetry, fixed with fewer, larger requests."
sources: ["https://learn.microsoft.com/azure/architecture/antipatterns/chatty-io/", "https://learn.microsoft.com/azure/architecture/antipatterns/extraneous-fetching/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chatty I/O antipattern

## Symptoms
- High latency and low throughput; users report long response times or timeouts from I/O contention.
- A large number of small requests to the same file, service or data store from one application instance.
- Applications that become I/O bound.

## Common causes
- Reading and writing individual records as distinct database requests, including an O/RM that implicitly fetches
  child records one at a time (the N+1 problem).
- A single logical operation implemented as a series of HTTP requests, such as one GET per property of a User object.
- Repeatedly reading or writing small amounts to a file; small writes can also fragment the file.

## Fixes
1. **Fetch in one query** instead of several smaller ones (the Azure example uses Entity Framework `Include` to
   replace a per-product loop with a single SELECT).
2. **Coarser web API operations**: one GET returning the User instead of one per property; this trades a larger body
   for fewer calls. For HTTP APIs, see bounded batch operations.
3. **Buffer writes in memory** and write once. A buffer is lost if the process crashes; for bursty or sparse data an
   external durable queue such as Event Hubs may be safer.
4. **Cache** data fetched from a service or database to avoid repeated requests.
5. **Split hot and cold data** so the frequently used part is returned alone.
6. Avoid the opposite antipattern, **extraneous fetching**: retrieving more than the operation needs, often an
   overcorrection for chattiness. Paginate and return only the fields needed.

## Steps
1. Monitor production to find operations with poor response times.
2. Load test each one and gather telemetry on the data access requests it makes, with per-request statistics.
3. Profile in a test environment; with an O/RM, trace the generated SQL.
4. Re-run the same load test after the change.

## Verify
- [ ] Requests per operation reduced and response time and throughput improved under the same load profile.

## Checked
2026-11-08. Confirmed against the Azure Architecture Center Chatty I/O antipattern page (causes, fixes, trade-offs,
detection steps, N+1 note, buffering and Event Hubs note, caching) and the Extraneous Fetching antipattern page
(definition, relation to chatty I/O, pagination). Removed: DynamoDB BatchGetItem, Redis MGET, Graph $batch,
`WHERE id IN`, views and stored queries, gateway aggregation and BFF suggestions, and per-call cost claims (not on
these pages).
Method: documentation only; no commands were run.

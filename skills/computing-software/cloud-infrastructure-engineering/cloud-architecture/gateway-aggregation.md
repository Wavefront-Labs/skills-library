---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.gateway-aggregation
name: gateway-aggregation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, api-gateway-patterns, gateway-aggregation, api-composition, fan-out, chatty-clients, graphql-federation, partial-response, mobile-latency]
level: practitioner
status: docs-checked
description: "Collapse many client round trips into one by aggregating backend calls at a gateway or composition layer: partial failure policy, resilience, placement and limits."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/gateway-aggregation", "https://microservices.io/patterns/data/api-composition.html", "https://www.apollographql.com/docs/federation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gateway aggregation

**Problem:** a client must call several back-end services to complete one task. Chattiness costs resources on each
request and hurts performance and scale, and separate requests over a high-latency cellular network are inefficient
and raise the chance of connectivity loss or incomplete responses.

**Solution:** the client sends one request (a package of sub-requests); the gateway decomposes it, calls the relevant
services, combines the results and returns one response.

## Steps
1. Identify chatty client flows (calls per screen or task, over high-latency networks).
2. Choose where aggregation lives. Lightweight composition, shaping and response assembly fit in the gateway (the Azure
   example uses API Management with the `send-request` policy). Custom domain logic, complex transformations or
   longer-running orchestration belong in a dedicated service behind the gateway, which also keeps aggregation's
   different resource needs from affecting routing and offloading. Microservices.io calls this an API Composer: it
   invokes the owning services and does an in-memory join. GraphQL federation (Apollo router with subgraphs) is a
   declarative alternative: the client makes one request and the router coordinates the API calls.
3. **Resilience**: bulkheads, circuit breaking, retry and timeouts; asynchronous I/O so a slow back end does not stall
   the app; load test the gateway so it does not cause cascading failures.
4. **Partial failure policy**, explicit per operation: return a partial response when missing data is acceptable, or
   fail the whole request when complete, consistent data is required. Clients must see predictable behaviour.
5. Consider cached data as a failover strategy.
6. Trace each call with correlation IDs and monitor request metrics and response sizes.

## Gotchas
- The gateway must not introduce coupling across back-end services.
- Place it near the back-end services to minimise latency.
- It can become a single point of failure or a bottleneck: size and scale it.
- Some compositions mean inefficient in-memory joins of large datasets; CQRS is the alternative.
- Not suitable to cut calls to one service across many operations (add a batch operation instead), nor when client and
  back ends are close and latency is not significant.

## Verify
- [ ] Client round trips per task are reduced (before/after measurement).
- [ ] With one optional back end down, the aggregate returns the agreed partial response within its timeout.

## Checked
2026-11-08. Confirmed against the Azure Gateway Aggregation pattern page (problem, solution, considerations, when to
avoid, API Management send-request example, partial-response decision, dedicated service behind the gateway),
microservices.io API Composition (API composer, in-memory join drawback, CQRS alternative) and Apollo Federation
introduction (router, single request, subgraphs). Removed as unstated: the 150 ms round-trip arithmetic, the claim
that plain gateways rarely aggregate well, BFF-per-experience advice, parallel fan-out with an overall deadline,
token exchange, DataLoader batching.
Method: documentation only; no commands were run.

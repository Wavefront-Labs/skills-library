---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.rate-limiting
name: rate-limiting
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, api-gateway-patterns, rate-limiting, throttling, token-bucket, sliding-window, quotas, http-429, retry-after, per-tenant-limits, distributed-rate-limiter, ratelimit-headers, throttling-pattern]
level: practitioner
status: docs-checked
description: "Protect services and enforce fair use with rate limits: algorithm choice, per-principal and per-tenant keys, 429 with Retry-After, IETF RateLimit headers, priority shedding."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/throttling", "https://learn.microsoft.com/azure/architecture/patterns/rate-limiting-pattern", "https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Throttling and rate limiting

Two directions: **inbound** (limit what an instance, tenant or the whole service can consume so it meets its
SLOs) and **outbound** (stay under a dependency's quota; see the Azure Rate Limiting pattern).

## Inbound
1. **Key**: per-principal limits need each request attributed to a principal (user or tenant) and resource use
   metered against it. Limiting per tenant stops one tenant monopolising resources; see the Azure page on
   measuring consumption per tenant.
2. **Algorithm** (Azure throttling page):
   | Algorithm | Property |
   |---|---|
   | Token bucket | allows bursts up to a configured size with a steady refill rate; suits gateways absorbing short spikes |
   | Leaky bucket | emits at a constant rate; suits back ends needing steady ingress |
   | Fixed window | simple, but admits back-to-back bursts at window boundaries |
   | Sliding window | smooths the boundary problem at the cost of more state |
3. **Response**: HTTP `429 Too Many Requests` when the caller exceeds the configured rate over a defined
   window. Include a `Retry-After` header and enough context to retry deliberately: name the limit exceeded,
   the affected scope, or a rate that would succeed.
4. **Headers**: the IETF httpapi draft defines `RateLimit-Policy` and `RateLimit` header fields so clients
   can see quotas. It is an Internet-Draft, so check its status before depending on it.
5. **Priority**: where requests differ in value, shed lower-value or more retryable work first, or defer
   lower-priority tenants and tell them to retry later; load leveling with a priority queue is the
   alternative.

## Outbound
Pace calls to stay below the provider's quota, and propagate back-pressure signals such as 429 with
`Retry-After`. Coordinate with retries: blind or aggressive retries add load and cause retry storms, so use a
limited number of retries with small random delays.

## Gotchas
- Limits without monitoring hide customer pain: record rejected requests per principal.
- Fixed windows allow bursts around window boundaries.
- Unexplained rejections do not help callers adapt.

## Verify
- [ ] Load one tenant beyond its limit: it receives 429s with `Retry-After`, and other tenants' latency is
      unchanged.
- [ ] Limits are documented per plan.

## Checked
2026-11-01. Confirmed against the Azure Throttling pattern page (per-principal limits, algorithm table, 429,
`Retry-After`, priority shedding, tenant example), the Azure Rate Limiting pattern page (retry coordination)
and the IETF draft (header names, Internet-Draft status). Removed: specific gateway products and policy
names (APIM, Envoy with Redis, Cloud Armor), the local versus distributed counter claims, the 503 load
shedding rule and the 2x burst figure, which these pages do not state. The Envoy page was not used.
Method: documentation only; no commands were run.

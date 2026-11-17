---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.per-customer-limits-and-quotas
name: per-customer-limits-and-quotas
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [per-customer-limits, customer-quota-enforcement, rate-limiting, token-bucket, handling-overload, envoy-rate-limit]
level: practitioner
status: docs-checked
description: "Enforce per-customer quotas so one client cannot overload a shared service: resource-based quota units, oversubscription, Envoy global rate limit service config and 429 behaviour."
sources: ["https://sre.google/sre-book/handling-overload/", "https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/rate_limit_filter", "https://github.com/envoyproxy/ratelimit", "https://datatracker.ietf.org/doc/html/rfc6585#section-4"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Per-customer limits and quotas

SRE Book "Handling Overload": when global overload occurs, the service should deliver errors only to
misbehaving customers while others remain unaffected. Owners provision capacity from negotiated usage and
define per-customer quotas to match those agreements.

## Quota unit
The book recommends measuring capacity directly in resources (for example CPU cores and memory) rather
than QPS, using "cost of a request" as a normalised measure of CPU time consumed. In most cases CPU
consumption alone works as the provisioning signal (memory pressure shows as CPU under garbage collection).
Its example limits are expressed in CPU seconds per second per customer.

## Oversubscription
The book's example quotas add up to more than the CPUs allocated; the owner relies on it being unlikely
that all customers hit their limits simultaneously.

## Related controls in the same chapter
- Client-side throttling: a client that sees many recent "out of quota" rejections caps its own outgoing
  traffic; excess requests fail locally without reaching the network.
- Criticality: when a customer runs out of global quota, a task rejects requests of a given criticality
  only if it is already rejecting all lower criticalities; per-customer limits can be set per criticality.

## Envoy global rate limit
The rate limit filter calls an external rate limit service. If any descriptor is over limit it returns 429
(configurable with `rate_limited_status`) and sets `x-envoy-ratelimited` unless disabled. With
`enable_retry_after_header` (off by default) the 429 carries `Retry-After`. On errors calling the service,
`failure_mode_deny: true` returns 500; with it false, requests are allowed through and counted as
`failure_mode_allowed`. Decide the fail-open or fail-closed choice explicitly.

Rate limit service config shape (envoyproxy/ratelimit README: a `domain`, `descriptors` with `key`, and
`rate_limit` with `unit` of second, minute, hour or day and `requests_per_unit`):
```yaml
domain: <DOMAIN>
descriptors:
- key: <DESCRIPTOR_KEY>
  rate_limit:
    unit: second
    requests_per_unit: <N>
```
Which request attributes become descriptors is set in the Envoy route configuration; see the filter page.

## Response semantics
RFC 6585 section 4 defines 429 Too Many Requests. Distinguish a per-customer over-quota rejection from
global service overload so clients know whether backing off or reducing their own usage is the fix.

## Verify
- [ ] Drive one customer past quota in a test: only that customer receives rejections.
- [ ] Rejections are visible per customer on a dashboard.

## Checked
2026-11-01. Confirmed against the SRE Book Handling Overload chapter, the Envoy rate limit filter page, the
envoyproxy/ratelimit README and RFC 6585 section 4 (title only). Removed: weighted request-unit and
concurrency options, edge/backend/client layer table, the route action snippet, `RESOURCE_EXHAUSTED`,
`RateLimit-*` headers, the 503-vs-429 rule, example limit numbers and the 3x quota load test.
Method: documentation only; no commands were run.

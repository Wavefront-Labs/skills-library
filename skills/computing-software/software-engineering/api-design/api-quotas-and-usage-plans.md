---
id: computing-software.software-engineering.api-design.api-quotas-and-usage-plans
name: api-quotas-and-usage-plans
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-quotas, usage-plans, rate-limiting, ratelimit-headers, api-monetization]
level: practitioner
status: docs-checked
description: "Define API quotas and usage plans per key or tenant: rate vs volume limits, RateLimit headers clients can read, 429 responses, API Gateway plans."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html", "https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/", "https://cloud.google.com/docs/quotas/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quotas and usage plans

## Kinds of limit
- **Rate limit**: restricts how fast a resource is consumed over a time period (Google Cloud "rate quota"). Protects the service from bursts.
- **Quota / allocation**: restricts how much of a resource you are given; Google Cloud also has concurrent quotas for long-running operations.
- Scope matters: Google Cloud quotas apply at project, folder or organisation level, and may be global, regional or zonal. Decide the partition (key, tenant, user) up front and document it.

## Usage plans (AWS API Gateway example)
- A usage plan uses API keys to identify clients and sets throttling and quota limits that are enforced per API key, aggregated across the stages in the plan.
- The limits are best-effort targets, not hard ceilings, so do not rely on them for cost control.
- API keys are not for authorization; use proper auth alongside them.
- Key name is at most 1024 characters; key value is 20 to 128 characters.
- Tier names, numbers and prices are your product decision; define them as data, not code.
- When endpoints differ hugely in cost, count cost units rather than raw requests (design choice; the IETF draft allows a quota unit other than requests).

## Telling clients (IETF draft, an Internet-Draft, not a standard)
`draft-ietf-httpapi-ratelimit-headers` (revision 11 when checked, expiring November 2026) defines two response fields:
- `RateLimit-Policy`: the quota policy the request consumes. Parameters: `q` (required quota), `qu` (quota unit, default `requests`), `w` (window in seconds), `pk` (partition key).
- `RateLimit`: the quota currently available. Parameters: `r` (required remaining quota), `t` (seconds until the window resets), `pk`.
```
HTTP/1.1 429 Too Many Requests
Retry-After: 30
RateLimit-Policy: "daily";q=10000;w=86400
RateLimit: "daily";r=0;t=30
```
The draft says clients must not treat a positive `r` as a guarantee that further requests will be served, that service-specific parameters should carry a vendor prefix, and that when `Retry-After` and `RateLimit` both appear, `Retry-After` takes precedence. It recommends 429 for exceeded limits and 503 when the server is overloaded. Neither field may appear in a trailer. Because it is a draft, treat header names and parameters as subject to change.

## Implementation notes (practice, not from the sources)
- Keep counters in a central store; accept a small overshoot rather than a global lock.
- Exhausted quota is a 4xx (429), never 500.
- Exempt health checks and internal callers via separate keys.

## Checked
2026-11-08. Confirmed by reading the AWS usage plans page, the Google Cloud Quotas overview, and the relevant parts of the IETF draft (abstract, sections 3 and 4, status-code recommendations; security and examples sections only skimmed). Removed (not in the sources): the Free/Pro/Enterprise tier table and figures, Apigee and Kong mentions, the `X-RateLimit-*` claim, Redis `INCR`, the 80/100% warning advice, the `GET /usage` endpoint and the 403 option.
Method: documentation only; no commands were run.

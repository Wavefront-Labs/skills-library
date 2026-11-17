---
id: computing-software.web-development.web-performance.origin-shield-and-tiered-caching
name: origin-shield-and-tiered-caching
category: computing-software
field: web-development
product: web-performance
tags: [origin-shield, tiered-caching, cdn-architecture, cache-hit-ratio, origin-offload]
level: advanced
status: docs-checked
description: "Reducing origin load with origin shields and tiered caching: how CDN tiers work, enabling them on Cloudflare, Fastly and CloudFront, shield location, and measuring origin offload."
sources:
  - https://developers.cloudflare.com/cache/how-to/tiered-cache/
  - https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/origin-shield.html
  - https://www.fastly.com/documentation/guides/concepts/shielding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Origin shield and tiered caching

Without tiering, each of a CDN's many edge PoPs fetches from your origin independently on a miss. A purge or a new deploy then causes a thundering herd of origin requests, and long-tail content has a poor hit ratio.

## 1. How it works
Lower-tier edge PoPs miss -> ask an upper-tier/shield PoP -> only the shield goes to origin. One origin fetch fills many edges, and the shield's larger cache keeps the long tail warm.

## 2. Enabling it
| CDN | Feature |
|---|---|
| Cloudflare | Smart Tiered Cache (dynamically selects the single closest upper tier for each origin; Cloudflare now lists it under Smart Shield) |
| AWS CloudFront | **Origin Shield** is an additional layer in the CloudFront caching infrastructure; you choose its region per origin |
| Fastly | Shielding: designate a shield POP per backend near the origin |

Choose the shield location nearest the origin (lowest RTT), not nearest the users.

## 3. Considerations
- Adds a hop on misses (slightly higher miss latency), much higher overall hit ratio.
- Multi-region origins: shield per origin region, or rely on smart topology.
- Costs: check your CDN's pricing page for shield charges.

## 4. Measure
- Origin requests per second and origin egress before/after (origin access logs or CDN "origin offload" metrics).
- Cache hit ratio by tier in CDN analytics; the cache-status response headers your CDN documents.
- Load-test a purge: watch origin RPS spike stay bounded.

## Verify
- [ ] Origin offload improved; purge does not overload origin; shield location documented next to origin region.

## Checked
2026-10-28 Confirmed on the fetched Cloudflare tiered cache page (Smart Tiered Cache picks the closest upper tier per origin; now under Smart Shield), the CloudFront Origin Shield page (an additional caching layer) and Fastly shielding (shield POP). Removed: plan-availability claims, the Akamai row, header names, hit-ratio target, billing wording, request-collapsing and stale-serving claims, the 'hundreds of PoPs' figure.
Method: documentation only; no commands were run.

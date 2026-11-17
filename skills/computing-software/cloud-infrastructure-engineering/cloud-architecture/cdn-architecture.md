---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cdn-architecture
name: cdn-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, caching-strategy, cdn-architecture, content-delivery, origin-shield, edge-caching, cache-hit-ratio, origin-protection]
level: practitioner
status: docs-checked
description: "Design CDN architecture: origins, edge caching and TTL, cache hit ratio, private content, TLS and WAF at the edge, using CloudFront, Front Door, Cloud CDN and Cloudflare docs."
sources: ["https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html", "https://learn.microsoft.com/azure/frontdoor/front-door-overview", "https://docs.cloud.google.com/cdn/docs/overview", "https://developers.cloudflare.com/cache/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# CDN architecture

## Steps
1. **Define origins.** CloudFront: an S3 bucket, MediaPackage channel or HTTP server (custom origin
   on EC2 or your own). Cloud CDN: Compute Engine VMs, Cloud Storage backend buckets, GKE Ingress
   or Gateway backends, behind a global external or classic Application Load Balancer. Front Door
   load balances and routes across origins with health probes and can reach origins privately via
   Azure Private Link. Keep S3 content private and serve it through signed URLs or signed cookies
   when access must be controlled (CloudFront).
2. **Set expiry.** Origin headers say how long objects stay cached. CloudFront default: 24 hours in
   an edge location, minimum 0 seconds, no maximum. In Cloud CDN, content can have a configurable
   expiration, e.g. content changing hourly should expire in under an hour. Cloudflare Cache Rules
   say which resources are cached and for how long; Purge removes cached files.
3. **Understand cache behaviour.** Cloud CDN caching is reactive: an object is stored only when a
   request passes through and the response is cacheable; caches cannot be preloaded except by
   requests. Eviction is unpredictable, so no request is guaranteed a hit; cache key
   configuration affects hit ratio (see Cloud CDN "Using cache keys"). Cloudflare offers Tiered
   Cache and Cache Reserve (persistent storage for longer retention).
4. **Security.** Front Door: SSL offload at the edge with integrated certificate management, free
   autorotated managed certificates, built-in layer 3-4 DDoS protection, an attached WAF
   including bot manager rules; Microsoft recommends DDoS Protection and a WAF for web workloads.
5. **Measure.** Cloud CDN reports cache hit ratio (percentage of requests served from cache) per
   origin in its console; also track partial hits (byte-range requests), cache fill and egress.

## Gotchas
- Cloud CDN allows requesting an object directly from the origin, bypassing the cache; for any CDN,
  verify the origin is not reachable around the edge (private link, signed access) if the WAF must
  not be bypassed.
- CloudFront bills data transfer out from edge locations and requests; transfer from AWS origins to
  CloudFront is free. Check each vendor's pricing page for current numbers.

## Verify
- [ ] Hit ratio is visible per origin and reviewed.
- [ ] Expiry is set deliberately for each content class.

## Checked
Confirmed against the four cited overview pages (CloudFront Introduction, Front Door overview, Cloud
CDN overview, Cloudflare Cache overview). Removed as not stated there: Origin Shield, specific
Cache-Control directives (immutable, s-maxage, stale-while-revalidate), cache-key header guidance,
the 90 percent hit-ratio target, Set-Cookie caching claim, HSTS and geo restriction advice,
micro-caching.
Method: docs-only read of cited pages, 2026-11-08

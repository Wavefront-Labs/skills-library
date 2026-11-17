---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cdn-cost-optimisation
name: cdn-cost-optimisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, architecting-for-cost, cdn-cost-optimisation, cdn, cache-hit-ratio, egress, cloudfront, origin-shield]
level: practitioner
status: docs-checked
description: "Use a CDN to cut egress and origin cost: raise cache hit ratio, cache-key hygiene, origin shield, compression, cache invalidation discipline and flat-rate plans for delivery."
sources: ["https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cache-hit-ratio.html", "https://aws.amazon.com/cloudfront/pricing/", "https://cloud.google.com/cdn/docs/best-practices", "https://learn.microsoft.com/azure/frontdoor/front-door-caching"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CDN offload to cut egress

Serving users through a CDN can offload origin servers and improve latency, and every cache hit
avoids an origin request. Whether it saves money depends on the provider's CDN and egress pricing
(see its pricing page) and above all on cache hit ratio.

## Why it can save
- AWS states that data transfer between CloudFront and your AWS origins is waived when serving
  traffic through CloudFront (stated on the flat-rate plan description; confirm on the pay-as-you-go
  pricing page for your account).
- Cached responses and collapsed duplicate requests mean fewer hits on origin servers, databases and
  other usage-billed services.
- CloudFront offers flat-rate monthly plans (a Free tier plus paid tiers with monthly request and
  data transfer allowances) and a custom pricing tier through sales; compare with pay-as-you-go.

## Steps
1. Measure: CDN cache hit ratio (requests and bytes), origin bytes, egress by distribution.
2. **Cache-key hygiene**: include only the query strings, headers and cookies that change the
   response. Every extra key fragments the cache.
   - CloudFront: forward only the query parameters your origin uses, with consistent case and
     parameter order (it caches `a=1&b=2` and `b=2&a=1` separately). Forward only needed cookies
     (each cookie value combination is cached separately); use separate cache behaviours for static
     and dynamic content. Avoid caching on `User-Agent`; use the CloudFront device-type headers.
   - Cloud CDN: the default cache key is the full request URL; use custom cache keys to omit host,
     protocol or query strings, e.g. disable query strings in the key for `/static/*`.
   - Azure Front Door: query string behaviour is Ignore, Use, or ignore/include specified parameters;
     parameter order does not matter.
3. **TTLs**: set the longest practical `Cache-Control: max-age` (shorter durations mean more origin
   revalidation); `stale-while-revalidate` and `stale-if-error` can help further on CloudFront.
   For versioned static assets, version the file name or add a query string (Cloud CDN's example is
   `file.ext?v=100`) rather than relying on invalidation.
4. **Origin shield** (CloudFront Origin Shield): one extra caching layer so all requests from edge
   locations and regional edge caches reach the origin from a single location.
5. **Compression**: Azure Front Door compresses at the edge (classic: dynamically, for eligible MIME
   types, when caching is on; its newer profiles support gzip and Brotli, preferring Brotli). If compression is
   not used, CloudFront lets you remove `Accept-Encoding` from the cache key via a blank custom
   origin header. Compress and size images at the origin (practice guidance).
6. **Move downloads** (installers, media, exports) behind the CDN with signed URLs where the
   provider supports them (Cloud CDN does).
7. **Review pricing options** for your CDN regularly, including flat-rate or committed plans.

## Gotchas
- Caching authenticated or personalised responses leaks data; vary correctly or bypass cache.
- A low-hit-ratio CDN in front of dynamic APIs adds a hop without offloading much.
- Cloud CDN advises invalidation only as a last resort (eventually consistent, rate limited);
  prefer versioned file names.

## Verify
- [ ] Byte and request hit ratio tracked per distribution, with a target you set.
- [ ] Origin egress and compute load fell after enabling or tuning the CDN.

## Checked
2026-11-08. Confirmed on the CloudFront cache hit ratio guide (TTLs, stale-while-revalidate, Origin Shield, query string, cookie and header guidance, Accept-Encoding), the CloudFront pricing page (flat-rate plans, waived transfer to AWS origins), the Cloud CDN best practices (custom cache keys, versioning, invalidation) and the Azure Front Door caching page (query string modes, gzip/Brotli).
Removed: claims that CDN egress per GB is generally at or below region egress, that committed CDN pricing is common, price classes, a free invalidation allowance, the `immutable` header example, Origin Shield equivalents for other CDNs and the 90% hit ratio target (none stated on the pages read). Prices are not quoted; see each vendor's pricing page.
Method: documentation only; no commands were run.

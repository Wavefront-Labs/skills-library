---
id: computing-software.cloud-infrastructure-engineering.aws.cloudfront-distributions
name: cloudfront-distributions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudfront, cdn, edge-caching, origin-access-control, oac, origins, origin-groups, cache-policy, origin-request-policy, response-headers-policy, cache-behaviors, ttl, invalidation, cache-hit-ratio, origin-shield, cloudfront-functions, lambda-at-edge, signed-urls, signed-cookies, key-groups, geo-restriction, vpc-origins, custom-origin-header, price-class, http3, brotli, real-time-logs, content-delivery]
level: practitioner
status: draft
description: "Build CloudFront distributions that cache: S3 origins with OAC, locked-down ALB origins, cache and origin-request policies, invalidation, edge functions, signed URLs, logging and cost."
sources: ["Amazon CloudFront Developer Guide - Restricting access to an Amazon S3 origin (OAC)", "Amazon CloudFront Developer Guide - Managed cache, origin request and response headers policies", "Amazon CloudFront Developer Guide - Invalidating files and managing how long content stays in the cache", "Amazon CloudFront Developer Guide - CloudFront Functions and Lambda@Edge", "Amazon CloudFront Developer Guide - Serving private content with signed URLs and signed cookies", "Amazon CloudFront Developer Guide - Using VPC origins and Origin Shield"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CloudFront distributions — edge caching that protects the origin

**Goal:** a distribution whose cache-hit ratio is above 90% for static content, whose
origins cannot be reached except through it, whose cache keys contain exactly the
inputs that change the response, and whose cost is dominated by edge delivery rather
than origin egress. Certificates come from `...aws.acm-certificates-and-private-ca`
(us-east-1); WAF attachment is in `...aws.waf-and-shield`.

## 1. Origins
- **S3 (REST endpoint `bucket.s3.<region>.amazonaws.com`)** with **Origin Access
  Control**: `create-origin-access-control --origin-access-control-config
  Name=…,SigningProtocol=sigv4,SigningBehavior=always,OriginAccessControlOriginType=s3`,
  attach to the origin, keep Block Public Access **on**, and give the bucket policy a
  single statement allowing `cloudfront.amazonaws.com` `s3:GetObject` with
  `"AWS:SourceArn": "arn:aws:cloudfront::<ACCT>:distribution/<ID>"`. OAC supports
  SSE-KMS (grant the CloudFront service principal `kms:Decrypt` with the same
  SourceArn) and signed `PUT`/`DELETE`. Legacy OAI cannot do either — migrate.
  The S3 *website* endpoint is a plain HTTP custom origin and cannot use OAC; use it
  only if you need S3 redirect rules.
- **ALB / custom origin**: HTTPS-only to origin, origin protocol policy `https-only`,
  and lock it down with either **VPC origins** (ALB/NLB/EC2 in private subnets, no
  public exposure at all; CloudFront reaches them via an ENI) or, for public ALBs, a
  **custom origin header** (`X-Origin-Secret: <random>`) checked by a WAF rule or
  listener rule on the ALB, plus the ALB security group limited to the
  `com.amazonaws.global.cloudfront.origin-facing` managed prefix list.
- **Origin groups**: primary + secondary with failover on `500,502,503,504` (and/or
  403/404 for S3) — only for `GET/HEAD/OPTIONS`; writes never fail over.
- **Origin Shield** (one extra regional cache layer in front of the origin, billed per
  request): enable it in the origin's region when many edge locations hit a small
  origin or when origin egress cost matters; it typically lifts origin-side hit ratio
  substantially.

## 2. Cache behaviors and the cache key
A behavior = path pattern (`/api/*`, `*.jpg`, default `*`) + origin + policies.
Order matters: first match wins; the default behavior is evaluated last.
- **Cache policy** decides the key and TTLs. Start from managed ones:
  `CachingOptimized` (static; no query/cookies/headers in key, Gzip+Brotli on),
  `CachingDisabled` (APIs), `CachingOptimizedForUncompressedObjects`. Custom policy
  when the response varies by something specific: include *only* those query strings
  (`?v=`), cookies (session id for personalised HTML) or headers (`Accept-Language`,
  `CloudFront-Viewer-Country`). Every extra key dimension multiplies cache entries and
  divides hit ratio.
- **Origin request policy** forwards things to the origin *without* keying on them:
  `AllViewer` (most ALB APIs), `AllViewerExceptHostHeader` (when the origin is an ALB
  whose listener rules match its own host), `CORS-S3Origin` (forwards `Origin` so S3
  CORS works while keying only on it in the cache policy).
- **Response headers policy**: `SecurityHeadersPolicy` (HSTS, X-Content-Type-Options,
  frame options) or a custom one adding CORS and `Cache-Control` overrides.
- TTLs: `MinTTL` ≤ origin `Cache-Control: max-age` ≤ `MaxTTL`; with no origin header
  `DefaultTTL` (86,400 s on managed policies) applies. Set `Cache-Control` at the
  origin (`max-age=31536000, immutable` for hashed filenames; `no-store` or
  `s-maxage=60` for HTML) so the policy rarely needs changing.
- Viewer protocol policy `redirect-to-https`; allowed methods `GET,HEAD,OPTIONS` for
  static behaviors, all seven for APIs (CloudFront never caches `POST`).

## 3. Invalidation vs versioning
- `aws cloudfront create-invalidation --distribution-id <ID> --paths "/index.html" "/assets/*"`
  — first 1,000 paths per month free, then per path; a wildcard counts as one path.
  Completion takes a few minutes; it does not purge browser caches.
- Prefer **content hashing** (`app.3f2a9c.js`) so files are immutable and only
  `index.html` (short TTL) ever needs invalidation. Use invalidation for mistakes, not
  as the deploy mechanism.
- **Continuous deployment**: a staging distribution + policy routes a weight or a
  header-selected slice of traffic to the new config; promote with
  `update-distribution-with-staging-config`.

## 4. Edge compute
| | CloudFront Functions | Lambda@Edge |
|---|---|---|
| Runs at | viewer request/response only | viewer + origin request/response |
| Runtime | JavaScript (restricted), < 1 ms, 10 KB code | Node.js/Python, up to 5 s viewer / 30 s origin, VPC-less, us-east-1 only |
| Use for | URL rewrites (`/about` → `/about/index.html`), header injection, redirects, JWT check with **KeyValueStore** | origin selection, body manipulation, auth that calls other services, image resizing |
| Cost | per million invocations, cheap | per request + duration, higher |
Functions cannot access the body or network; Lambda@Edge replicas are deleted slowly
when you detach them (hours), and logs land in the region nearest the edge.

## 5. Private content and restrictions
- **Signed URLs** (single file, e.g. a download) or **signed cookies** (a whole path,
  e.g. a video manifest + segments) require a **key group** containing a public key
  you upload (`create-public-key` with an RSA-2048 PEM) and `TrustedKeyGroups` on the
  behavior. Sign with the private key in your app (SDK `CloudFrontSigner`); policies
  carry expiry, optional start time and source IP. Rotate by adding a second key to
  the group before removing the first.
- **Geo restriction** (allow/deny list of countries) is per distribution; for finer
  logic use `CloudFront-Viewer-Country` in a function.
- Field-level encryption is niche; most teams use TLS to origin plus application
  encryption.

## 6. Delivery, logs, cost
- Alternate domain names need an ACM cert in **us-east-1**; TLS 1.2_2021 security
  policy; enable **HTTP/3**; price class `PriceClass_100` (NA+EU) if your users are
  there — the edge cost difference is real.
- **Standard logs** to S3 (legacy) or **standard logging v2** to CloudWatch Logs/S3/
  Firehose with field selection; **real-time logs** via Kinesis Data Streams when you
  need seconds. Watch `CacheHitRate`, `OriginLatency`, `5xxErrorRate` in CloudWatch
  (metrics live in us-east-1).
- Egress to CloudFront from S3/ALB is **free**; the per-GB edge delivery rate is what
  you pay, plus per-request fees. CloudFront's free tier (1 TB/month) is permanent.

## Gotchas
- S3 returns **403, not 404**, for missing objects when the policy grants only
  `GetObject`; map custom error responses (403 → `/404.html`, TTL 10 s) or also grant
  `ListBucket` to the OAC (then 404s surface).
- Forwarding the `Host` header to an S3 origin breaks it (S3 cannot match); to an ALB
  with host-based rules it is required.
- Changing a distribution takes minutes to deploy (`Status: Deployed`); CLI
  `update-distribution` needs the full config with the current `ETag` — `get-distribution-config`,
  edit, send back.
- CORS failures through CloudFront are almost always the cache: `Origin` not in the
  cache key means a cached response without `Access-Control-Allow-Origin` is served to
  the browser. Use `CORS-S3Origin`/`CORS-CustomOrigin` policies.
- `Cache-Control: no-cache`/`no-store`/`private` from the origin are honoured only
  when `MinTTL` is 0; a non-zero MinTTL caches them anyway.
- Two distributions cannot share the same alternate domain name; moving a CNAME
  between them requires the move-CNAME procedure or a wildcard trick.

## Verify
- [ ] Bucket is not publicly accessible; `curl https://bucket.s3.<region>.amazonaws.com/file` returns 403, via CloudFront returns 200 with `x-cache: Hit from cloudfront` on the second request.
- [ ] `CacheHitRate` ≥ 90% for static behaviors after warm-up; cache key contains only variables the response depends on.
- [ ] ALB origin rejects direct requests lacking the origin secret header (or is unreachable from the internet with VPC origins).
- [ ] A deploy changes only hashed filenames; one invalidation of `/index.html` completes in under 5 minutes.
- [ ] Signed URL expires on schedule (403 after expiry) and a rotated key still signs.

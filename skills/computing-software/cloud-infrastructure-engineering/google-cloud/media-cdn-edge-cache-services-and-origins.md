---
id: computing-software.cloud-infrastructure-engineering.google-cloud.media-cdn-edge-cache-services-and-origins
name: media-cdn-edge-cache-services-and-origins
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, media-cdn, media-cdn-edge-cache-services, edge-cache-origins, video-streaming, signed-tokens, network-services]
level: practitioner
status: docs-checked
description: "Deploy Media CDN for streaming and large downloads: EdgeCacheOrigin and EdgeCacheService YAML, route rules and cache policy, dual-token signed requests, and when to use Cloud CDN."
sources: ["https://docs.cloud.google.com/media-cdn/docs/quickstart", "https://docs.cloud.google.com/media-cdn/docs/use-dual-token-authentication"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Media CDN: EdgeCacheService and origins

Media CDN is for high-throughput media delivery. You define an **EdgeCacheOrigin** and an **EdgeCacheService**
(see the quickstart for the exact resources and prerequisites).

## Origin
```bash
gcloud edge-cache origins create media-origin --origin-address="gs://<BUCKET>" \
  --max-attempts=2 --failover-origin=media-origin-backup
```
`--origin-address` is the origin's address (a bucket URL in this example); see the quickstart for other forms.

## Service
```yaml
# service.yaml
name: vod
routing:
  hostRules:
  - hosts: ["video.example.com"]
    pathMatcher: routes
  pathMatchers:
  - name: routes
    routeRules:
    - priority: 1
      matchRules: [{prefixMatch: "/"}]
      origin: media-origin
      routeAction:
        cdnPolicy:
          cacheMode: CACHE_ALL_STATIC
          defaultTtl: 3600s
```
```bash
gcloud edge-cache services import vod --source=service.yaml
gcloud edge-cache services describe vod
```
Point DNS (`video.example.com`) at the service's addresses shown by `describe`.

## Signed requests
Dual-token authentication: short-lived signed token on the manifest URL, longer token in a cookie
or URL prefix for segments; keys in an `EdgeCacheKeyset` (Ed25519 public keys, or HMAC-SHA1/HMAC-SHA256 shared keys held in Secret Manager;
the docs recommend Ed25519 and HMAC only for compatibility with other CDNs).

## Cache operations
```bash
gcloud edge-cache services invalidate-cache vod --path="/titles/123/*"
```

## Verify
- [ ] A second request for the same asset is served from cache (check the service's logs).

## Checked
2026-10-28. Confirmed against the Media CDN quickstart and dual-token authentication pages: origin and service creation commands, route YAML
(`hostRules`, `pathMatchers`, `prefixMatch`, `cacheMode: CACHE_ALL_STATIC`, `defaultTtl`), `EdgeCacheKeyset` and signature algorithms.
Commands verified against the gcloud reference. Removed: YouTube infrastructure and allowlisting claims, origin types, security-policy and certificate
fields, metric and log names, shielding note.
Method: documentation only; no commands were run.

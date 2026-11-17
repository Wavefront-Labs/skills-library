---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-cdn-and-caching
name: cloud-cdn-and-caching
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-cdn, cdn, cache-keys, cache-modes, cache-control, ttl-overrides, negative-caching, signed-urls-cdn, signed-cookies, cache-invalidation, backend-bucket, media-cdn, edge-cache, origin-shield, cache-hit-ratio, serve-stale, compression, bypass-cache-on-request-headers]
level: practitioner
status: docs-checked
description: "Make Cloud CDN actually cache: cache modes and TTLs, cache keys, negative caching, serve-stale, signed URLs and cookies for private content, invalidation."
sources: ["https://cloud.google.com/cdn/docs/overview", "https://cloud.google.com/cdn/docs/caching", "https://cloud.google.com/cdn/docs/using-cache-modes", "https://cloud.google.com/cdn/docs/using-cache-keys", "https://cloud.google.com/cdn/docs/using-signed-urls", "https://cloud.google.com/cdn/docs/invalidating-cached-content", "https://cloud.google.com/media-cdn/docs/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud CDN and caching

**Goal:** static and semi-static responses served from Google's edge with a hit ratio you
can see, private assets served only with a signature, and a bad deploy purged in seconds.

## 1. Enable
```bash
gcloud compute backend-services update web-bs --global --enable-cdn --cache-mode=CACHE_ALL_STATIC \
  --default-ttl=3600 --max-ttl=86400 --client-ttl=600 --negative-caching \
  --negative-caching-policy='404=60,410=120' --serve-while-stale=86400
gcloud compute backend-buckets create assets --gcs-bucket-name=<P>-assets --enable-cdn --cache-mode=FORCE_CACHE_ALL --default-ttl=604800
```

## 2. Cache modes (the decision)
| Mode | Caches | Use |
|---|---|---|
| `USE_ORIGIN_HEADERS` | only responses with valid `Cache-Control: public, max-age=…`/`s-maxage` | app controls caching precisely |
| `CACHE_ALL_STATIC` | static MIME types (images, CSS, JS, fonts, video) even without headers, plus anything origin marks cacheable; respects `private`/`no-store` | default for most sites |
| `FORCE_CACHE_ALL` | everything, ignores `private`/`no-store` | backend buckets, immutable asset paths **only** — it ignores `private`/`no-store`, so never use it on per-user or API responses |
- TTL precedence: `client-ttl` (what browsers get) ≤ `default-ttl` (when origin gives none) ≤ `max-ttl` (cap on origin value). Origin `Cache-Control: no-store`/`private` wins unless FORCE_CACHE_ALL.
- Responses with `Set-Cookie` (in the MIME-type path), `private`/`no-store` (unless FORCE_CACHE_ALL), a `Vary` value outside the allowed list, or a non-cacheable status code are not cached. Even FORCE_CACHE_ALL does not override `Vary`.
- **Negative caching**: cacheable error statuses include 404, 405, 410, 421, 451 and 501; use short TTLs to protect the origin from scanners.
- **Serve-while-stale**: keep serving an expired object for N seconds while revalidating — origin outages become invisible for static content.

## 3. Cache keys
`--cache-key-include-protocol --cache-key-include-host --no-cache-key-include-query-string` or `--cache-key-query-string-whitelist=v,lang`; `--cache-key-include-http-header=X-Device` / `--cache-key-include-named-cookie=ab_variant` (Envoy LBs). Every included dimension multiplies cache entries, so leave tracking query parameters out of the key.
`bypass-cache-on-request-headers` sends requests that carry a matching header around the cache for all cache modes, even FORCE_CACHE_ALL; many matching requests means many misses.

## 4. Private content
- **Signed URLs**: `gcloud compute backend-services add-signed-url-key web-bs --key-name=k1 --key-file=key.txt` (a 16-byte secret key, base64url encoded); sign the URL with HMAC-SHA1 over the raw 16-byte key (`gcloud compute sign-url` or a library). `--signed-url-cache-max-age` controls edge TTL for signed objects. FORCE_CACHE_ALL overrides that maximum age.
- **Signed cookies** for whole-path access (HLS/DASH streams). Rotate keys by adding `k2`, switching signing, then deleting `k1`.
- URL prefix signing lets one signature cover a manifest + segments.

## 5. Invalidate and observe
- `gcloud compute url-maps invalidate-cdn-cache web-map --path '/static/app-*.js'` (path/wildcard suffix, host optional). Prefer **versioned filenames** (long TTL) and invalidate only HTML.
- Logs: `resource.type="http_load_balancer"` request logs (see the Cloud CDN logging page for the cache fields); metrics filtered by `cache_result`, where `cache_result!="DISABLED"` limits charts to CDN-enabled backends.
- **Media CDN** is a separate product for video and large-file delivery; see its own docs.

## Gotchas
- `Vary: Accept-Encoding` is fine; `Vary: User-Agent` or `Cookie` makes nearly everything a miss (Cloud CDN only caches responses whose `Vary` lists headers on the allowed list in the caching page, such as `Accept`, `Accept-Encoding`, `Origin`, `X-Goog-Allowed-Resources` and `Sec-Fetch-Dest`/`Mode`/`Site`, or headers in the cache key).
- `FORCE_CACHE_ALL` caches every successful response regardless of `private`/`no-store`. Keep API and static content on separate backend services so a mode change on one cannot leak the other.
- Dynamic compression (`--compression-mode=AUTOMATIC`) needs the origin to send uncompressed; double compression breaks.
- Invalidation does not purge browser caches; `client-ttl` is what the user keeps.

## Verify
- [ ] Two requests for a static asset: second shows a cache hit in the LB logs.
- [ ] An `Authorization`-bearing request is `cacheDecision: bypassed` and never served to another user.
- [ ] Signed URL works until it expires, then is refused; a tampered path is refused.
- [ ] Hit ratio dashboard for the static backend rises after warm-up; the `DISABLED` share is explained by headers you intend.

## Checked
2026-10-28. Confirmed against the Cloud CDN caching, cache modes and signed URLs pages: cache modes and FORCE_CACHE_ALL behaviour, cacheable status codes, the Vary allowed list, bypass-on-header behaviour, HMAC-SHA1 with a raw 16-byte key, `--signed-url-cache-max-age`, `cache_result!="DISABLED"`. All gcloud commands and flags passed check_commands. Removed: the 5 TB figure, invalidation rate, Media CDN throughput, fill service account name, log field names and cache_result values not seen in the fetched pages.
Method: documentation only; no commands were run.

---
id: computing-software.cloud-infrastructure-engineering.google-cloud.enabling-cloud-cdn-on-backends-with-gcloud
name: enabling-cloud-cdn-on-backends-with-gcloud
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-cdn, backend-service-enable-cdn, cdn-enable-gcloud, backend-buckets, cache-invalidation]
level: practitioner
status: docs-checked
description: "Enable Cloud CDN on backend services and backend buckets with gcloud: cache modes, TTLs, negative caching, cache keys, serve-while-stale, invalidation, and signed URL keys."
sources: ["https://cloud.google.com/cdn/docs/using-cdn", "https://cloud.google.com/cdn/docs/caching", "https://cloud.google.com/cdn/docs/invalidating-cached-content", "https://cloud.google.com/cdn/docs/using-signed-urls", "https://cloud.google.com/sdk/gcloud/reference/compute/backend-services/update", "https://cloud.google.com/sdk/gcloud/reference/compute/backend-buckets/create", "https://cloud.google.com/load-balancing/docs/https/https-logging-monitoring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enabling Cloud CDN on backends with gcloud

Cloud CDN is a flag on a backend of a global external Application Load Balancer.

## 1. Backend service (dynamic origin)
```bash
gcloud compute backend-services update web-be --global --enable-cdn \
  --cache-mode=USE_ORIGIN_HEADERS \
  --negative-caching --negative-caching-policy='404=60,410=60' \
  --serve-while-stale=86400 \
  --cache-key-include-protocol --cache-key-include-host \
  --cache-key-query-string-whitelist=page,lang
```

## 2. Backend bucket (static assets in GCS)
```bash
gcloud compute backend-buckets create assets-bb --gcs-bucket-name=BUCKET --enable-cdn \
  --cache-mode=CACHE_ALL_STATIC --default-ttl=3600 --max-ttl=86400 --client-ttl=3600
```
Cloud Storage objects should be publicly readable to be cached. With private bucket access enabled you must set the `FORCE_CACHE_ALL` cache mode to cache private content from the bucket.

## 3. Cache modes
| Mode | Caches |
|---|---|
| `USE_ORIGIN_HEADERS` | successful responses that set valid cache directives and caching headers; others are forwarded from the origin |
| `CACHE_ALL_STATIC` | successful static-content responses plus origin responses with valid cache directives; the default for CDN-enabled backends created with gcloud or the REST API |
| `FORCE_CACHE_ALL` | unconditionally caches successful responses, overriding origin directives; not appropriate for per-user content (error responses may also be cached) |

## 4. Invalidate
```bash
gcloud compute url-maps invalidate-cdn-cache web-um --path="/css/*" --host=www.example.com --async
```
`url-maps invalidate-cdn-cache` also takes `--global` and `--tags` (cache tags). Prefer versioned file names (`app.3f9a.js`) with long TTLs over frequent invalidation.

## 5. Signed URLs/cookies
```bash
head -c 16 /dev/urandom | base64 | tr +/ -_ > key.txt
gcloud compute backend-services add-signed-url-key web-be --global --key-name=k1 --key-file=key.txt
```

## Gotchas
- `FORCE_CACHE_ALL` on an app that sets cookies can leak one user's page to another.
- Response bodies larger than 10 MiB are cached only if the origin supports byte range requests (up to 100 GiB); otherwise they are delivered but not cached.
- For signed URLs or cookies, `FORCE_CACHE_ALL` overrides the signed-URL cache maximum age.

## Verify
- [ ] `gcloud compute backend-services describe web-be --global --format='value(enableCDN,cdnPolicy.cacheMode)'` shows the settings; load balancer log entries for repeat requests show `statusDetails` of `response_from_cache`.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found incomplete: the cache modes table omitted that CACHE_ALL_STATIC is the default for gcloud and REST created backends and that FORCE_CACHE_ALL can cache error responses; the 10 MB statement was incomplete (10 MiB without byte ranges, 100 GiB with).
- Confirmed (gcloud reference): `backend-services update --enable-cdn --cache-mode --negative-caching --negative-caching-policy --serve-while-stale --cache-key-include-protocol --cache-key-include-host --cache-key-query-string-whitelist`; `backend-buckets create --gcs-bucket-name --enable-cdn --cache-mode --default-ttl --max-ttl --client-ttl`; `url-maps invalidate-cdn-cache --path --host --async --tags`; `add-signed-url-key --key-name --key-file`.
- Confirmed (signed URLs page): the 128-bit base64 key command `head -c 16 /dev/urandom | base64 | tr +/ -_`. Confirmed (Compute API discovery): enableCDN and cdnPolicy fields. Confirmed (load balancer logging page): statusDetails value response_from_cache.
- Removed: the rate-limited invalidation remark, the cache-key-change claim, the public-or-signed bucket wording and the Age header and cacheHit verification (not found in the pages read).

Method: documentation only; no commands were run.

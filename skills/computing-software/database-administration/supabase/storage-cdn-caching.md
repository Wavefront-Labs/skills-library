---
id: computing-software.database-administration.supabase.storage-cdn-caching
name: storage-cdn-caching
category: computing-software
field: database-administration
product: supabase
tags: [storage, cdn, caching, cf-cache-status, cache-hit]
level: practitioner
status: docs-checked
description: "How Supabase Storage CDN caching behaves: public vs private hit rates, eviction, and reading cf-cache-status HIT and MISS."
sources:
  - https://supabase.com/docs/guides/storage/cdn/fundamentals
  - https://supabase.com/docs/guides/storage/uploads/standard-uploads
  - https://supabase.com/docs/guides/storage/serving/downloads
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: predict and debug cache behaviour for Storage assets.

All assets uploaded to Supabase Storage are cached on a CDN, and all Storage API requests are routed to the CDN first. The origin is the storage server in the same region as your project.

Hit rates:
- Public buckets need no authorization, so they get a better hit rate: a second user requesting the same object from the same region gets a cache hit.
- Private buckets check permissions per user. Two users with different policies requesting the same object from the same region both get a miss.

Eviction: an object can be evicted from a regional CDN node if it has not been requested there for a while, even with a long cache control duration.

Debugging: read the `cf-cache-status` response header.
- `MISS`: the node did not have the object and went to the origin.
- `HIT`: the object was served directly from the CDN.

Practical consequences:
- Serve widely shared assets from a public bucket.
- Overwriting an object (upsert) risks stale content because of CDN propagation; upload to a new path instead (stated on the upload pages).
- Previously accessed signed URLs can still be served from CDN cache after revocation; purge the cache to clear them.

## Checked

Confirmed against the CDN fundamentals page: all assets cached, origin in the project region, public vs private hit behaviour, eviction note, cf-cache-status MISS and HIT. Upsert staleness advice confirmed on the uploads page. The purge advice for revoked signed URLs is confirmed on the URL signing keys page. Nothing removed.

Method: docs-checked 2026-11-09 against the Supabase docs source for guides/storage/cdn/fundamentals, guides/storage/uploads/standard-uploads and guides/storage/security/signing-keys (apps/docs/content on GitHub master), read in full.

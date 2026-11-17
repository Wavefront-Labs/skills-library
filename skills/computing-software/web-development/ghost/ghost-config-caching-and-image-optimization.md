---
id: computing-software.web-development.ghost.ghost-config-caching-and-image-optimization
name: ghost-config-caching-and-image-optimization
category: computing-software
field: web-development
product: ghost
tags: [ghost, caching, cache-control, redis, image-optimization, performance, config]
level: advanced
status: docs-checked
description: "Tune Ghost caching: Cache-Control maxAge per area, the Redis cache adapter, compression and upload image optimization."
sources:
  - https://github.com/TryGhost/docs/blob/main/config.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reduce load on a busy Ghost site.

HTTP caching: the `caching` config sets `maxAge` in the `Cache-Control` header for public responses. Keys and defaults from the docs: `frontend` 0, `contentAPI` 0, `robotstxt` 3600, `sitemap` 3600, `sitemapXSL` 86400, `wellKnown` 86400, `cors` 86400, `publicAssets` 31536000, `301` 31536000, `customRedirects` 31536000. Example: `"caching": {"contentAPI": {"maxAge": 10}}` adds `Cache-Control: public, max-age=10` to Content API responses, useful for high-volume sites with rarely changing content.

Redis cache adapter: change an adapter from Memory to Redis so the cache survives restarts and is not limited by RAM. Redis must be set up and running in addition to Ghost. Example for image sizes: `"adapters": {"cache": {"imageSizes": {"adapter": "Redis", "ttl": 3600, "keyPrefix": "image-sizes:"}}}`. `ttl` is in seconds.

Compression: `"compress": true` is the default.

Image optimization on upload: resize to 2000px max width, compress JPEGs to 80 percent quality and strip metadata, keeping the original with an `_o` suffix. Disable with `"imageOptimization": {"resize": false}`.

Verify: `curl -I` a Content API URL and check the Cache-Control header.

## Checked

2026-11-04. Confirmed: every caching key and default maxAge, the contentAPI example, Redis adapter example and ttl in seconds, compress default, image optimization details and the resize switch (configuration page). Removed: the "cache or CDN in front instead of multiple nodes" scaling note.

Method: documentation only; no commands were run.

---
id: computing-software.networking-hardware-and-wireless.haproxy.response-caching-small-objects
name: response-caching-small-objects
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, cache-section, cache-use, cache-store, total-max-size, haproxy-cache]
level: practitioner
status: docs-checked
description: "Enable HAProxy's built-in small-object cache with a cache section, cache-use, cache-store and tune sizes, with Vary and storage limits."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# response caching small objects
HAProxy's cache is designed for small objects (favicon, CSS and similar): a minimalist low-maintenance cache in RAM, in a memory area shared between all threads and split in 1 kB blocks. The key is a hash of the Host header and the URI. When the memory is needed, the oldest objects are deleted first, regardless of their expiry. Objects served from the cache show `<CACHE>` as the server name in the log.

```
cache static
    total-max-size 256        # megabytes of RAM, maximum 4095
    max-object-size 1048576   # bytes
    max-age 300               # seconds
    process-vary on
backend be_app
    mode http
    http-request cache-use static
    http-response cache-store static
    http-response set-header X-Cache %[res.cache_hit,iif(HIT,MISS)]
```
- `total-max-size` is mandatory. `max-object-size` must not exceed half of `total-max-size` (default: a 256th of the cache size); larger objects are not cached.
- `max-age` is the maximum expiration: the lowest of `s-maxage`/`max-age` from the response `Cache-Control` and this value. The default is 60 seconds.
- `process-vary` defaults to off, in which case any response with a `Vary` header is never cached. When on, the secondary key is built from `accept-encoding`, `referer` and `origin` only; `max-secondary-entries` (default 10) limits secondary entries per primary key.
- Neither stored nor delivered: responses that are not 200, not cacheable, or without an explicit expiration (`s-maxage`, `max-age` or `Expires`) or validator (`ETag` or `Last-Modified`); objects whose Content-Length plus headers exceeds `max-object-size`; `Vary` on an unmanaged header; requests that are not GET, below HTTP/1.1, or that carry an `Authorization` header.
- `cache-use <name>` is mandatory for storing too, because it computes the cache hash; if you use a condition for both actions, put it on `cache-use` first. `cache-store` stores the response headers at that point, so other `http-response` rules can modify headers before or after storage. Conditions are allowed on both, for example `if { path_beg /static/ }`.
- `res.cache_hit` is true when the response was built from a cache entry; `res.cache_name` returns the cache name.
- `show cache` on the Unix socket shows cache status (management guide section on socket commands).

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual, chapter 6 (Cache): intro, limitations, `cache`, `total-max-size`, `max-object-size`, `max-age`, `max-secondary-entries`, `process-vary`, the proxy-section text, the `cache-use`/`cache-store` actions, `res.cache_hit` and `res.cache_name`, and `iif`. Removed: the claims about `Cookie` requests being bypassed, `Content-Length` and `HEAD` handling, `tune.bufsize` linkage, URL purge/`purge cache`, reload behaviour, the `Age` header and `show stat` verification, and the "classic leak" paragraph. The `show cache` pointer is from the manual's chapter 6 text; the management guide was not read. Read as sections of the manual only.
Method: documentation only; no commands were run.

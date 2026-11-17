---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mod-expires-caching-headers
name: mod-expires-caching-headers
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-expires, expiresactive, expiresbytype, cache-control, max-age]
level: practitioner
status: docs-checked
description: "Generate Expires and Cache-Control max-age headers with ExpiresActive, ExpiresDefault and ExpiresByType, access vs modification base and wildcard types."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_expires.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_expires
Generates `Expires` and the `max-age` part of `Cache-Control`; other Cache-Control directives need `mod_headers`.

## Directives
- `ExpiresActive` default `Off`; `On` enables generation. It does not guarantee a header, and an existing `Expires` (CGI, proxied origin) is left alone.
- `ExpiresDefault` for all documents; `ExpiresByType MIME-type` overrides per type, and wildcards work (`image/gif`, then `image/*`, then default).

## Base
- `A`/`access`/`now`: expiry relative to the client's access, so each client differs.
- `M`/`modification`: all caches expire together.

```apache
ExpiresActive On
ExpiresDefault "access plus 1 month"
ExpiresByType text/html "access plus 1 month 15 days 2 hours"
ExpiresByType image/gif "modification plus 5 hours 3 minutes"
ExpiresByType image/* "access plus 1 month"
```
Units: years, months, weeks, days, hours, minutes, seconds. Legacy numeric form: `ExpiresByType image/gif A2592000`.

## Caveats
- Modification-based expiry sends no `Expires` for content without a file on disk.
- `max-age` is expiry time minus request time, from the same calculation as `Expires`.

## Checked
2026-11-04. Confirmed against the mod_expires reference: ExpiresActive default and caveats, ExpiresByType wildcard order, A/M base times, interval syntax and units, numeric form, modification-based caveat, max-age calculation. Nothing removed.
Method: documentation only; no commands were run.

---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.http-profile
name: http-profile
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, http-profile, x-forwarded-for, insert-xff, http-headers]
level: practitioner
status: draft
description: "Configure the BIG-IP HTTP profile to insert X-Forwarded-For, redirect rewrite, header limits and fallback host."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-local-traffic-manager-implementations.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HTTP profile: headers, X-Forwarded-For and compression

```
tmsh create ltm profile http http_xff defaults-from http insert-xff-header enabled xff-header-name X-Forwarded-For
tmsh modify ltm profile http http_xff header-erase "X-Powered-By" header-insert "X-Frame-Options: SAMEORIGIN" redirect-rewrite matching
tmsh modify ltm virtual vs_web profiles add { http_xff }
tmsh modify ltm profile http http_xff max-header-size 32768 fallback-host sorry.example.com fallback-status-codes add { 500 503 }
```
- `insert-xff-header` (named `insert-xff` in older docs; confirm on your version) adds the client IP so a SNAT'd backend can still log it. A header already present from an upstream proxy is appended to, not replaced; strip untrusted ones with an iRule `HTTP::header remove X-Forwarded-For` first.
- `redirect-rewrite` (`none|all|matching|nodes`) rewrites `Location:` headers that expose private node addresses.
- `header-erase` and `header-insert` apply to server responses/requests globally for the VS; use iRules or local traffic policy for conditional edits.
- A VS with an HTTP profile performs full L7 parsing and enables iRules `HTTP_REQUEST` events, cookie persistence, compression and OneConnect.
- Gotcha: `request-chunking` and `response-chunking` set to `preserve` can break clients when the pool sends a different framing; rechunk/unchunk is the default that works for most.
- Add `accept-xff enabled` only when trusting an upstream proxy, else clients can spoof their source address.

Verify: `curl -sI https://vip/ -H 'X-Forwarded-For: 1.2.3.4'`, and in a backend log confirm the header holds the real client address.

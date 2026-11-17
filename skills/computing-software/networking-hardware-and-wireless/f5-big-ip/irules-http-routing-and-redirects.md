---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.irules-http-routing-and-redirects
name: irules-http-routing-and-redirects
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, irules-routing, http-redirect, pool-selection]
level: practitioner
status: draft
description: "Route requests by URI or Host, redirect HTTP to HTTPS and edit headers with BIG-IP iRules."
sources:
  - https://clouddocs.f5.com/api/irules/HTTP__uri.html
  - https://clouddocs.f5.com/api/irules/HTTP__header.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# iRules for HTTP routing, redirect and header edits

```
when HTTP_REQUEST {
  switch -glob [string tolower [HTTP::host]] {
    "api.example.com"  { pool pool_api }
    "www.example.com"  { if { [HTTP::uri] starts_with "/img/" } { pool pool_static } else { pool pool_web } }
    default            { HTTP::respond 404 content "unknown host" }
  }
  HTTP::header insert X-Via "bigip"
  HTTP::header replace X-Forwarded-Proto "https"
}
```
```
when HTTP_REQUEST {
  HTTP::redirect "https://[getfield [HTTP::host] : 1][HTTP::uri]"
}
```
- Attach the redirect rule to a port 80 VS. `HTTP::redirect` sends a 302; for a permanent redirect use `HTTP::respond 301 Location "https://..."`.
- `HTTP::host` can include a port; `getfield [HTTP::host] : 1` strips it. Use `HTTP::path` (no query) and `HTTP::query` for URL parts, `URI::` commands for decoding.
- `pool` selects a pool for this request; with OneConnect or HTTP keep-alive, call `LB::detach` or enable OneConnect so the next request can go elsewhere.
- Do not forward `X-Forwarded-For` blindly; remove with `HTTP::header remove`.
- Gotcha: `HTTP::respond` and `HTTP::redirect` end the request processing; later code in the same event still runs unless you `return`.
- Local traffic policies cover the same cases with less CPU; prefer them for plain host/URI switching.

Verify: `curl -sI -H 'Host: api.example.com' http://vip/` and look at `X-Via`; `tmsh show ltm virtual vs_web` and pool counters show where each request went.

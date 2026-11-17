---
id: computing-software.networking-hardware-and-wireless.haproxy.cookie-persistence-sticky-sessions
name: cookie-persistence-sticky-sessions
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, cookie, sticky-sessions, persistence, insert-indirect-nocache]
level: practitioner
status: docs-checked
description: "Pin HTTP clients to a HAProxy server with the cookie keyword (insert, prefix, rewrite, indirect, nocache, dynamic) or stick tables on an app cookie."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cookie persistence sticky sessions
Cookie persistence needs no table: HAProxy adds a cookie holding the server's identifier. There can be only one persistence cookie per HTTP backend, and it may be declared in `defaults`. The value is the one given after `cookie` on each `server` line; a server without one sets no cookie.

```
backend be_app
    balance roundrobin
    cookie SRV insert indirect nocache httponly secure attr "SameSite=Lax"
    server a 10.0.0.11:8080 check cookie a
    server b 10.0.0.12:8080 check cookie b
```
Modes (mutually exclusive): `insert` has HAProxy create a session cookie when the client lacks a valid one; `prefix` completes an existing application cookie such as `JSESSIONID` with the server id; `rewrite` modifies a cookie the server provides (not advised for new deployments). Options: `indirect` sends no cookie to a client that already has a valid one and, with `insert`, removes the cookie from requests so the server never sees it (avoid it with `prefix`); `nocache` tags a cacheable response non-cacheable when a cookie is inserted, recommended with `insert` when a cache sits in front; `postonly` inserts only on POST responses; `preserve` lets the server emit its own cookie (with `insert`/`indirect`); `httponly` and `secure` add those attributes; `domain`, `maxidle` and `maxlife` (seconds) bound scope and age; `attr <value>` adds any other attribute and may be repeated; `dynamic` builds a per-server session cookie from the server's IP, port and the secret from the backend `dynamic-cookie-key`.

Non-cookie alternative: stick on an app value:
```
stick-table type string len 32 size 1m expire 30m
stick on req.cook(JSESSIONID)
stick store-response res.cook(JSESSIONID)
```
If the pinned server is down, clients with a stale cookie can stay stuck to it; `option redispatch` lets HAProxy break cookie persistence and send the request to a working server.

Verify: `curl -si http://lb/` shows a `Set-Cookie: SRV=...` header; send `-H 'Cookie: SRV=b'` and confirm in the log that server `b` served it.

## Checked
2026-11-03. Confirmed against configuration.html: the `cookie` keyword and every option above, `option redispatch`, `stick-table`/`stick on`/`stick store-response`. Removed: the exact `Cache-Control: private` claim for `nocache`, "dynamic avoids exposing topology", "default behaviour for cookie when check marks it down", the "attr needs 2.x confirm" note, the long-server-names header-size note, and the `path=/` in the sample output.
Method: documentation only; no commands were run.

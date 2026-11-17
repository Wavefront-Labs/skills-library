---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.cookie-persistence
name: cookie-persistence
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, persistence, cookie-persistence, insert-mode]
level: practitioner
status: draft
description: "Configure BIG-IP HTTP cookie persistence (insert, rewrite, passive), encryption and timeouts and verify the cookie."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-local-traffic-manager-implementations.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cookie persistence

```
tmsh create ltm persistence cookie ck_app defaults-from cookie method insert cookie-name APPSRV expiration 0 cookie-encryption required cookie-encryption-passphrase 'xxx' httponly enabled secure enabled always-send enabled
tmsh modify ltm virtual vs_web persist replace-all-with { ck_app { default yes } } fallback-persistence source_addr
```
- `method insert` (default): BIG-IP adds `Set-Cookie: BIGipServer<pool>=<encoded ip.port.0000>`. `rewrite` replaces a blank cookie the app sends; `passive` reads a cookie the app sets itself (hash, cookie-hash). `hash` mode uses an attribute of the app cookie.
- Needs an HTTP profile on the VS. The default encoding reveals the member's IP and port; set `cookie-encryption required` (confirm on your version) so internal addresses do not leak.
- `expiration 0` makes a session cookie (browser lifetime); a positive timer sets `expires=`. The profile `timeout` governs the BIG-IP side only for hash methods.
- `always-send enabled` re-issues the cookie on every response, extending lifetime.
- Gotcha: the cookie value is a pool-specific member address; if a member is removed or the pool name changes, clients go to a new member. Cookie persistence does not work for non-HTTP.

Verify: `curl -sI https://vip/ | grep -i set-cookie` for `BIGipServerpool_web=`; repeat with `-b` and confirm the same `X-Backend` header. For chaining use `tmsh show ltm persistence persist-records` (cookie persistence has no records).

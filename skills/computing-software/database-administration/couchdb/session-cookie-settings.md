---
id: computing-software.database-administration.couchdb.session-cookie-settings
name: session-cookie-settings
category: computing-software
field: database-administration
product: couchdb
tags: [authentication, cookies, session-timeout, secret, same-site]
level: practitioner
status: docs-checked
description: "Configure CouchDB cookie sessions in [chttpd_auth]: timeout, secret rotation, persistent cookies, cookie_domain, same_site, and hash_algorithms."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/auth.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since 3.2 these live in `[chttpd_auth]` (previously `[couch_httpd_auth]`).

- `timeout`: seconds since the last request before a session expires (page example 600).
- `secret`: signs cookies and proxy tokens. Change it any time: new cookies use the new value and the previous one is cached for the `timeout` duration. Set it on all nodes at once, though CouchDB tolerates discrepancies since nodes share their secrets. Easiest rotation: enable config auto-reload and update each node's `.ini`.
- `allow_persistent_cookies`: when `true`, sets Max-Age and Expires so browsers keep the cookie across restarts.
- `cookie_domain`: the `AuthSession` cookie `domain` attribute; empty by default.
- `same_site`: non-empty adds `SameSite` (`none`, `lax` or `strict`).
- `auth_cache_size`: userctx objects cached in memory (example 50).
- `hash_algorithms` (3.3): comma-separated HMAC list, for example `sha256, sha`. New sessions use the first; all can validate. Avoid `md4` and `md5`.

## Checked

2026-11-04. Confirmed against the CouchDB config/auth page ([chttpd_auth]): the 3.2 move from [couch_httpd_auth], timeout, secret rotation notes, allow_persistent_cookies, cookie_domain, same_site values, auth_cache_size, hash_algorithms (3.3) with first-hash and md4/md5 guidance. Nothing removed.

Method: documentation only; no commands were run.

---
id: computing-software.web-development.fastapi.http-basic-auth
name: http-basic-auth
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, security, http-basic, httpbasiccredentials, compare-digest, timing-attack, www-authenticate]
level: practitioner
status: docs-checked
description: "Add HTTP Basic Auth to a FastAPI route with HTTPBasic, compare credentials using secrets.compare_digest on UTF-8 bytes, and return 401 with WWW-Authenticate."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/advanced/security/http-basic-auth.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP Basic Auth

Goal: simplest browser-prompted authentication.

## Method
- Import `HTTPBasic` and `HTTPBasicCredentials`; create the scheme with `HTTPBasic()` and use it as a dependency. It returns `HTTPBasicCredentials` with `username` and `password`.
- With no credentials the app returns 401 plus `WWW-Authenticate` with value `Basic` (optional `realm`), which makes the browser show its login prompt.
- Compare using the standard library `secrets.compare_digest()`. It needs `bytes` or ASCII-only `str`, so encode username and password as UTF-8 bytes first (otherwise names like `Sebastian` with an accent fail).
- Reason: a plain `==` returns at the first differing character, so response time leaks how many leading characters were right; an attacker can automate guesses. `compare_digest` takes the same time either way.
- On bad credentials raise `HTTPException` with status 401 and the `WWW-Authenticate` header so the browser asks again.

## Verify
Open the route in a browser (prompt appears) and test a wrong password (401).

## Checked

2026-11-08: Read the HTTP Basic Auth page (HTTPBasic, 401 with WWW-Authenticate Basic and realm, secrets.compare_digest on UTF-8 bytes, timing-attack explanation). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08

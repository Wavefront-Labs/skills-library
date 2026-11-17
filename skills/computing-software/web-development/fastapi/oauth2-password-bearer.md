---
id: computing-software.web-development.fastapi.oauth2-password-bearer
name: oauth2-password-bearer
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, security, oauth2, password-flow, bearer-token, oauth2passwordbearer, token-url]
level: practitioner
status: docs-checked
description: "Protect FastAPI routes with OAuth2PasswordBearer: what tokenUrl means, what the dependency returns, and when it answers 401 by itself."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/security/first-steps.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OAuth2PasswordBearer

Goal: require a bearer token on a path operation.

## Method
- Create `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")` and use it as a dependency with `Depends`; the function receives the token as a `str`.
- `tokenUrl` is the URL the client uses to send `username` and `password` and get a token. It does not create that endpoint; you write the path operation yourself. The relative URL `token` (same as `./token`) resolves against where the API is hosted (`https://example.com/api/v1/` gives `https://example.com/api/v1/token`), which keeps it working behind a proxy.
- The name `tokenUrl` matches the OpenAPI spec.
- The dependency looks for the `Authorization` header with value `Bearer ` plus the token. If absent or not Bearer, it answers 401 itself, so your function always has a token string. It does not verify the token.
- Because it inherits from `fastapi.security.oauth2.OAuth2` and `SecurityBase`, FastAPI adds the security scheme to OpenAPI, giving the docs an Authorize button and lock icon.

## Setup note
Form data needs `python-multipart`; it is installed with `fastapi[standard]` but not with plain `fastapi`.

## Verify
Call the route without the header, expect 401; with `Authorization: Bearer foobar` the function runs.

## Checked

Method: docs-only read of cited pages, 2026-11-08

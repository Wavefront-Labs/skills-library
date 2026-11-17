---
id: computing-software.web-development.litestar.litestar-custom-authentication
name: litestar-custom-authentication
category: computing-software
field: web-development
product: litestar
tags: [litestar, security, authentication, abstractauthenticationmiddleware, exclude-from-auth, exclude-patterns, middleware]
level: practitioner
status: docs-checked
description: "Subclass Litestar AbstractAuthenticationMiddleware and control which routes skip auth using exclude regex patterns and the exclude_from_auth opt key."
sources: [https://docs.litestar.dev/latest/usage/security/abstract-authentication-middleware.html, https://docs.litestar.dev/latest/usage/security/excluding-and-including-endpoints.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar custom authentication and exclusions

Goal: write your own authentication middleware and choose which endpoints it protects.

## Method

Subclass `AbstractAuthenticationMiddleware` and implement async `authenticate_request`, returning an `AuthenticationResult` with `user` (any value, including `None`) and optional `auth` (default `None`):

```python
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult
from litestar.connection import ASGIConnection

class CustomAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:
        auth_header = connection.headers.get(API_KEY_HEADER)
        if not auth_header:
            raise NotAuthorizedException()
        ...
        return AuthenticationResult(user=user, auth=token)

auth_mw = DefineMiddleware(CustomAuthenticationMiddleware, exclude="schema")
app = Litestar(route_handlers=[...], middleware=[auth_mw])
```

The values become `request.user` / `request.auth` for HTTP handlers and `socket.user` / `socket.auth` for websockets (type them as `Request[MyUser, MyToken, State]`). The same works in dependencies.

Excluding routes:
- Opt key: `@get("/unsecured", exclude_from_auth=True)` skips auth for that handler.
- Backend config (`SessionAuth`, `JWTAuth`, `JWTCookieAuth`): `exclude` takes a string or list of regex patterns matched against the full path, unanchored. `/schema` matches any path containing it; anchor with `^`: `exclude=[r"^/login", r"^/signup", r"^/schema"]`.
- Rename the opt key with `exclude_opt_key="no_auth"` (default `exclude_from_auth`), then `@get("/unsecured", no_auth=True)`.
- Inverted (protect only `/secured`): `exclude=[r"^(?!.*\/secured$).*$"]`.

## Gotchas

- Passing `/` as an exclude pattern disables authentication for all routes, since as a regex it matches every path.

## Verify

Per the example, a request without the expected header raises `NotAuthorizedException`; routes marked `exclude_from_auth=True` respond without it.

## Checked

2026-11-07. Read the full cited page(s) (usage/security/abstract-authentication-middleware.html, usage/security/excluding-and-including-endpoints.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.

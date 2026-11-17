---
id: computing-software.web-development.litestar.litestar-rate-limit-sessions
name: litestar-rate-limit-sessions
category: computing-software
field: web-development
product: litestar
tags: [litestar, middleware, rate-limit, sessions, session-middleware, proxy, cookie-backend, server-side-sessions]
level: practitioner
status: docs-checked
description: "Set up Litestar RateLimitConfig (including behind a proxy) and client-side or server-side session middleware."
sources: [https://docs.litestar.dev/latest/usage/middleware/builtin-middleware.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar rate limiting and sessions

Goal: add rate limiting and cookie or store-backed sessions.

## Method

Rate limit (follows the IETF RateLimit draft headers). Only `rate_limit` is required: a tuple of unit (`second`, `minute`, `hour`, `day`) and integer quota.

```python
from litestar.middleware.rate_limit import RateLimitConfig
rate_limit_config = RateLimitConfig(rate_limit=("minute", 1), exclude=["/schema"])
app = Litestar(route_handlers=[handler], middleware=[rate_limit_config.middleware])
```

Clients are identified by their address by default. Behind a proxy that is the proxy's address. Do not trust `X-FORWARDED-FOR` directly because clients can spoof it to dodge limits; instead use a middleware that updates the client address securely, such as uvicorn's `ProxyHeaderMiddleware` or hypercorn's `ProxyFixMiddleware`.

Client-side sessions (`ClientSideSessionBackend`, AES encryption, cookie splitting) need `pip install 'litestar[cryptography]'`:

```python
from os import urandom
from litestar.middleware.session.client_side import CookieBackendConfig
session_config = CookieBackendConfig(secret=urandom(16))
app = Litestar(route_handlers=[...], middleware=[session_config.middleware])
```

The example uses a 16-byte (128-bit) key; in real use inject the secret from the environment. In handlers: `request.session`, `request.set_session({...})`, `request.clear_session()`.

Server-side sessions store data in a Litestar store and keep only a session ID cookie:

```python
from litestar.middleware.session.server_side import ServerSideSessionConfig
from litestar.stores.file import FileStore
app = Litestar(
    middleware=[ServerSideSessionConfig().middleware],
    stores={"sessions": FileStore(path=Path("session_data"))},
)
```

Supported stores: memory, file, Redis, Valkey. Both kinds share most cookie configuration (see `BaseBackendConfig`).

## Verify

With the page's session example, `POST /session` then `GET /session` returns `{"has_session": true}`; after `DELETE /session` it returns false.

## Checked

2026-11-07. Read the full cited page(s) (usage/middleware/builtin-middleware.html) and the example files they include, and confirmed the claims in this skill against that text. Changed 'AES-GCM encryption' to 'AES encryption', the page's wording.

Method: documentation only; no commands were run.

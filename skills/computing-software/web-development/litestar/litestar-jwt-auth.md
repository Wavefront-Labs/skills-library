---
id: computing-software.web-development.litestar.litestar-jwt-auth
name: litestar-jwt-auth
category: computing-software
field: web-development
product: litestar
tags: [litestar, security, jwt, jwtauth, jwtcookieauth, oauth2, token, authentication]
level: practitioner
status: docs-checked
description: "Configure Litestar JWTAuth, JWTCookieAuth and OAuth2PasswordBearerAuth with retrieve_user_handler, custom Token classes, and issuer or audience checks."
sources: [https://docs.litestar.dev/latest/usage/security/jwt.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar JWT security backends

Goal: add JWT authentication to a Litestar app.

## Method

Install: `pip install 'litestar[jwt]'` (pulls pyjwt and cryptography).

Backends:
- `JWTAuth` (`litestar.security.jwt`): sends and expects the token in a header.
- `JWTCookieAuth`: inherits `JWTAuth` but uses a cookie.
- `OAuth2PasswordBearerAuth`: inherits `JWTCookieAuth`, for OAuth 2.0 bearer password flows; takes `token_url`, e.g. `token_url="/login"`.

Pattern from the page's example:

```python
from litestar.security.jwt import JWTAuth, Token

async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> User | None:
    return MOCK_DB.get(token.sub)   # sync or async both work

jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=environ.get("JWT_SECRET", secrets.token_hex()),
    exclude=["/login", "/schema"],
)

@post("/login")
async def login_handler(data: JSONBody[User]) -> Response[User]:
    return jwt_auth.login(identifier=str(data.id), token_extras={"email": data.email}, response_body=data)

app = Litestar(route_handlers=[login_handler, ...],
               on_app_init=[jwt_auth.on_app_init], openapi_config=openapi_config)
```

`on_app_init` injects the JWT middleware and the OpenAPI security scheme. Alternatively `middleware=[jwt_auth.middleware]`. In handlers, `request.user` is the retrieved user and `request.auth` is the `Token`.

- Custom token: subclass `Token` and set `token_cls=CustomToken` on the backend. Fields are converted from JSON with basic type conversions only; for complex types (Pydantic, attrs, custom `type_decoders`) override `Token.encode` and `Token.decode`.
- Issuer and audience: `accepted_issuers=[...]` and `accepted_audiences=[...]`; a mismatch raises `NotAuthorizedException` (401).
- Custom validation: override `Token.decode_payload`, returning the decoded payload dict.
- Revocation: keep a list of revoked tokens and check it during authentication.

## Verify

In a protected handler, the page's example asserts that `request.user` is an instance of your user class and `request.auth` is a `Token`.

## Checked

2026-11-07. Read the full cited page(s) (usage/security/jwt.html) and the example files they include, and confirmed the claims in this skill against that text. Replaced a verify step the page does not show with the page example's isinstance assertions.

Method: documentation only; no commands were run.

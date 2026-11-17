---
id: computing-software.web-development.django-ninja.django-ninja-jwt-bearer-auth-from-scratch
name: django-ninja-jwt-bearer-auth-from-scratch
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, tutorial-auth, jwt, httpbearer, hs256, refresh-token, request-auth]
level: advanced
status: docs-checked
description: "Issue and verify HS256 JWT access and refresh tokens with the standard library and protect a whole NinjaAPI with an HttpBearer authenticator."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/tutorial/part-4.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: JWT login with no extra packages, applied API-wide with login endpoints left open.

## Token module
A JWT is three base64url strings joined by dots: header, claims payload, and an HMAC-SHA256 signature over the first two using `settings.SECRET_KEY`.
```python
def b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def b64decode(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))

def sign(message: str) -> str:
    digest = hmac.new(settings.SECRET_KEY.encode(), message.encode(), hashlib.sha256).digest()
    return b64encode(digest)

def create_token(user_id: int, token_type: str, lifetime: int) -> str:
    header = b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    claims = {"sub": str(user_id), "type": token_type, "exp": int(time.time()) + lifetime}
    payload = b64encode(json.dumps(claims).encode())
    return f"{header}.{payload}.{sign(f'{header}.{payload}')}"

def decode_token(token: str, token_type: str) -> dict | None:
    try:
        header, payload, signature = token.split(".")
    except ValueError:
        return None
    if not hmac.compare_digest(signature.encode(), sign(f"{header}.{payload}").encode()):
        return None
    claims = json.loads(b64decode(payload))
    if claims["type"] != token_type or claims["exp"] < time.time():
        return None
    return claims
```
Lifetimes: access 15 minutes, refresh 7 days. `type` is a custom claim so a refresh token cannot call the API. Verify the signature before reading claims, always verify with HS256 regardless of the token's `alg` (rules out `"alg": "none"`), compare with `hmac.compare_digest`, and return `None` for any failure.

## Authenticator
```python
class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        claims = decode_token(token, "access")
        if claims is None:
            return None
        return User.objects.filter(id=claims["sub"], is_active=True).first()
```
`HttpBearer` reads `Authorization: Bearer <token>`. What `authenticate()` returns becomes `request.auth`; `None` yields a `401`. Returning the `User` makes `request.auth` the current user, and deactivated users stop working immediately.

## Protect everything, open the login routes
```python
api = NinjaAPI(title="TaskFlow API", auth=JWTAuth())
api.add_router("/auth", "accounts.api.router")

router = Router(tags=["auth"], auth=None)   # accounts/api.py
```
`auth` resolves from most specific to least: operation, router, API. `auth=None` opts out.

Endpoints on the open router:
- `signup`: 409 via `HttpError` if the username exists; run `validate_password()` and turn `ValidationError` messages into `HttpError(400, " ".join(e.messages))`; `User.objects.create_user(...)`.
- `token`: Django's `authenticate(username=..., password=...)`, else `HttpError(401, "Invalid username or password")`; return `{access, refresh}`.
- `refresh`: `decode_token(payload.refresh, "refresh")`, check the user is still active, else `HttpError(401, "Invalid or expired refresh token")`; return a new pair. An access token is refused here because its `type` claim is wrong.

Without a token, other endpoints return `401` with `{"detail": "Unauthorized"}`. In Swagger UI the operations show a lock and an Authorize button; paste the access token without the `Bearer ` prefix.

## Checked

2026-11-07: Confirmed against tutorial Part 4 (JSON Web Tokens from scratch, Protecting the API, Try it): the token helpers, lifetimes, `type` claim, constant-time compare, `JWTAuth(HttpBearer)`, `auth` precedence, the three open endpoints and their error strings, the 401 body and the Swagger lock. Nothing removed.

Method: documentation only; no commands were run.

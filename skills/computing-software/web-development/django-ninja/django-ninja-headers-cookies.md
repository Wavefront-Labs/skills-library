---
id: computing-software.web-development.django-ninja.django-ninja-headers-cookies
name: django-ninja-headers-cookies
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, headers-cookies, header, cookie, request-headers, alias]
level: intro
status: docs-checked
description: "Read request headers and cookies in Django Ninja with Header and Cookie, including aliases, defaults, schemas and constraints."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/headers-cookies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Read headers and cookies in Django Ninja

Goal: parse request headers/cookies like query parameters.

```python
from ninja import Cookie, Header, NinjaAPI, P

@api.get("/agent")
def get_agent(request, user_agent: Header[str]):
    return {"user_agent": user_agent}

@api.get("/session")
def get_session(request, session_id: Cookie[str]):
    return {"session_id": session_id}
```

- Header names match case-insensitively with underscores treated as hyphens (`user_agent` matches `User-Agent`); this comes from Django's `HttpRequest.headers`.
- Cookie names match exactly (from `request.COOKIES`, a plain dict).

## Required, optional, typed
No default means required; a missing one returns `422` with `"loc": ["header", "user_agent"]`. Give it a default to make it optional, combined with `X | None` when the header might not be sent: `user_agent: Header[str | None] = None`. Values arrive as strings and are converted: `x_rate_limit: Header[int] = 100` with `X-Rate-Limit: 42` gives int `42`.

## Aliases

```python
def request_id(request, req_id: Header[str, P(alias="X-Request-ID")]): ...
def weapon(request, weapon: Cookie[str, P(alias="preferred-weapon")]): ...
```

## Group in a Schema

```python
class ClientInfo(Schema):
    user_agent: str = Field(None, alias="User-Agent")
    x_request_id: str | None = None

@api.get("/client-info")
def client_info(request, client: Header[ClientInfo]):
    return client.model_dump()
```

`Header[ClientInfo]` is the preferred style; the older `client: ClientInfo = Header(...)` still works. `Cookie[...]` works the same for a group of cookies.

## Constraints
Same as `Query`, passed in `P(...)`: `gt`/`ge`/`lt`/`le` for numbers; `min_length`, `max_length`, `pattern` for strings; plus `title`, `description`, `example`/`examples`, `deprecated`, `include_in_schema`. For example `x_api_token: Header[str, P(min_length=32, max_length=64)]`.

## Raw access
`request.headers` and `request.COOKIES` are always available. Undeclared headers/cookies are ignored. Setting response headers or cookies is covered by a separate page (temporal response).

## Checked

2026-11-07: Confirmed against the Headers & Cookies guide: header name folding, exact cookie names, 422 `loc`, optional and typed values, aliases, `Header[ClientInfo]` grouping, constraints and raw `request` access. Corrected: examples that used `x: str = Header(...)`, `Header(None)`, `Header(100)` and `Header(..., alias=...)` now use the page forms `Header[str]`, `Header[str | None] = None`, `Header[int] = 100` and `Header[str, P(alias=...)]`; constraints now go in `P(...)`; the older `ClientInfo = Header(...)` form is stated as still working, as on the page.

Method: documentation only; no commands were run.

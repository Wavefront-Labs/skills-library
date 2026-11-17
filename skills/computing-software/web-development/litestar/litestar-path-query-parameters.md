---
id: computing-software.web-development.litestar.litestar-path-query-parameters
name: litestar-path-query-parameters
category: computing-software
field: web-development
product: litestar
tags: [litestar, parameters, path-params, query-params, from-path, from-query, header, cookie, type-coercion]
level: practitioner
status: docs-checked
description: "Declare Litestar path, query, header and cookie parameters with FromPath/FromQuery markers, path slot types, defaults and coercion."
sources: [https://docs.litestar.dev/latest/usage/routing/parameters.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar path and query parameters

Goal: inject typed request parameters into handlers.

## Method

Four sources, each with a marker form and an equivalent `Annotated` form:
`FromQuery[T]` = `Annotated[T, QueryParameter()]`, and likewise `FromPath`/`PathParameter`, `FromHeader`/`HeaderParameter`, `FromCookie`/`CookieParameter` (all in `litestar.params`). Prefer markers unless extra configuration is needed.

```python
@get("/{user_id:int}")
async def handler(user_id: FromPath[int], limit: FromQuery[int],
                  token: FromHeader[str], session: FromCookie[str]) -> None: ...
```

- Path slots use `{param_name:param_type}`. Supported types: `date`, `datetime`, `decimal`, `float`, `int`, `path`, `str`, `time`, `timedelta`, `uuid`.
- The slot type coerces first; the handler annotation can request a further coercion (slot `int`, handler `datetime`).
- If the handler does not use a path parameter, omit it from the signature; it is still validated and in the OpenAPI schema.
- Header and cookie names default to the parameter name (headers match case-insensitively). For names such as `X-API-KEY` use `Annotated[str, HeaderParameter(name="X-API-KEY")]` or `CookieParameter(name="session-id")`.
- Required, optional, nullable: no default means required; a default makes it optional; `| None` makes it nullable but still required unless defaulted; `required=False` needs a default. Example: `param: FromQuery[str | None] = None`.
- Raw values arrive as strings and are coerced to the marker's inner type (`FromHeader[int]`, `FromCookie[datetime]`).

## Gotchas

- Path parameters are always required; a default only fills in when the handler is registered on several paths (for example `["/items", "/items/{id:int}"]`).
- Path parameters cannot be declared on application layers.

## Verify

For `@get("/") def index(param: FromQuery[str | None] = None)`, the page's example is requested with `/` and `/?param=goodbye`; the handler receives `None` and `"goodbye"` respectively.

## Checked

2026-11-07. Read the full cited page(s) (usage/routing/parameters.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.

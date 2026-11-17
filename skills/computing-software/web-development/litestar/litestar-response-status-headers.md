---
id: computing-software.web-development.litestar.litestar-response-status-headers
name: litestar-response-status-headers
category: computing-software
field: web-development
product: litestar
tags: [litestar, status-code, headers, cookies, cache-control, etag, response-headers, response-cookies]
level: practitioner
status: docs-checked
description: "Set Litestar status codes, layered response_headers and response_cookies, and the predefined CacheControlHeader and ETag headers."
sources: [https://docs.litestar.dev/latest/usage/responses.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar response status, headers, cookies, cache control and ETag

Goal: control the status code and response metadata at handler, controller, router and app layers.

## Method

Status: `@get("/resources", status_code=HTTP_202_ACCEPTED)` with constants from `litestar.status_codes` (or `http.HTTPStatus`). Defaults: POST 201, DELETE 204, GET/PATCH/PUT 200. With `@route` and several methods the default is 200.

Headers: `response_headers` exists on every layer; values merge from all layers.

```python
from litestar.datastructures import ResponseHeader
@get("/handler-path", response_headers=[
    ResponseHeader(name="my-local-header", value="local header", description="local level header")])
```

`ResponseHeader` adds OpenAPI attributes such as `description` and `documentation_only`; a plain mapping also works: `@get(response_headers={"my-header": "header-value"})`.

Dynamic headers: either return a `Response` and set its `headers` (document the header with `ResponseHeader(name=..., documentation_only=True)` and no value), or use an `after_request` handler on a layer and document the header on that same layer.

Cookies: `response_cookies` on every layer; a lower layer redeclaring the same key overrides the higher one. A mapping works when only key and value are needed: `@get(response_cookies={"my-cookie": "cookie-value"})`. Output looks like `Set-Cookie: local-cookie=local value; Path=/; SameSite=lax`. Dynamic cookies follow the same two patterns as headers.

Predefined headers (kwarg or class attribute on any layer; nearer layer overrides):
- `cache_control=CacheControlHeader(max_age=86_400, public=True)`, or `CacheControlHeader(no_store=True)`; the page's app value `max_age=2_628_288` is 1 month.
- `etag=ETag(value="bar")`, weak: `ETag(value="bar", weak=True)` gives `W/"bar"`. For a dynamically computed etag, use `ETag(documentation_only=True)` on the handler and set the `etag` header on the returned `Response` yourself.

## Gotchas

- Status codes below 100, and 204 and 304, allow no body: a return annotation other than `None` raises `ImproperlyConfiguredException`.
- A `ResponseHeader` that only documents a dynamically set header takes `documentation_only=True` and no value.

## Verify

In the page's cache-control example, the app-level `/population` response carries `max-age=2628288`, the controller route `max-age=86400`, and the `no-store` route `no-store`.

## Checked

2026-11-07. Read the full cited page(s) (usage/responses.html) and the example files they include, and confirmed the claims in this skill against that text. Narrowed the documentation_only gotcha to what the page says.

Method: documentation only; no commands were run.

---
id: computing-software.web-development.fastapi.cors-middleware
name: cors-middleware
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, cors, corsmiddleware, allow-origins, preflight, credentials, origin]
level: practitioner
status: docs-checked
description: "Configure CORSMiddleware in FastAPI: allowed origins, methods, headers, credentials rules, wildcard limits, preflight handling and defaults."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/cors.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CORS

Goal: let a browser frontend on another origin call the API.

## Concepts
- An origin is protocol + domain + port, so `http://localhost`, `https://localhost` and `http://localhost:8080` are three origins.
- The browser sends an `OPTIONS` preflight; the backend must list the frontend origin in its allowed origins.

## Method
`app.add_middleware(CORSMiddleware, allow_origins=[...], ...)`, imported from `fastapi.middleware.cors` (also available from `starlette.middleware.cors`).

## Arguments (defaults restrictive)
- `allow_origins`, `allow_origin_regex`.
- `allow_methods`: default `['GET']`; `['*']` for all standard methods.
- `allow_headers`: default `[]`; `Accept`, `Accept-Language`, `Content-Language`, `Content-Type` always allowed for simple requests.
- `allow_credentials`: default `False`. If `True`, none of origins, methods or headers may be `['*']`; list them explicitly.
- `expose_headers`: default `[]`. `max_age`: default `600`.

## Behaviour
- `"*"` origin allows no credentials (cookies, Authorization headers), so list origins explicitly.
- Preflight (`OPTIONS` with `Origin` and `Access-Control-Request-Method`): the middleware answers with CORS headers and a `200` or `400`.
- Simple requests (with `Origin`): passed through with CORS headers added.
- Custom response headers a browser should read must be in `expose_headers`.

## Verify
Call from the frontend origin and inspect the CORS response headers.

## Checked

Read the full tutorial/cors.md source page. Confirmed the origin definition and example origins, the OPTIONS preflight, wildcard limits, every CORSMiddleware argument and its default (allow_methods ['GET'], allow_headers [], allow_credentials False, expose_headers [], max_age 600), the always-allowed simple-request headers, preflight and simple-request handling (200 or 400), and the fastapi.middleware.cors / starlette.middleware.cors imports. No claims removed.

Method: docs-only read of cited pages, 2026-11-08

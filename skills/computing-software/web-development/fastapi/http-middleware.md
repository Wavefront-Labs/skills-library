---
id: computing-software.web-development.fastapi.http-middleware
name: http-middleware
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, middleware, call-next, add-middleware, execution-order, process-time]
level: practitioner
status: docs-checked
description: "Write FastAPI HTTP middleware with @app.middleware and call_next, add a timing header, and predict the execution order of stacked middlewares."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/middleware.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Middleware

Goal: run code on every request and response.

## Method
- Decorate a function with `@app.middleware("http")`. It receives `request` and `call_next`.
- `response = await call_next(request)` passes the request to the path operation and returns its response; modify the response before returning.
- Code before `call_next` runs before the path operation; code after runs once the response exists. Example in the docs: an `X-Process-Time` header using `time.perf_counter()`, which can be more precise than `time.time()`.
- Custom proprietary headers can use the `X-` prefix. For a browser client to see them, add them to CORS `expose_headers`.
- `Request` can also be imported from `starlette.requests`.

## Order
Each middleware added (decorator or `app.add_middleware()`) wraps the app; the last added is outermost and runs first on the request path and last on the response path.
```
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```
Request: B then A then route. Response: route then A then B.

## Timing notes
- Exit code of dependencies with `yield` runs after the middleware.
- Background tasks run after all middleware.

## Checked

Read the whole Middleware tutorial page. Removed the Verify step, which the page does not state.

Method: docs-only read of cited pages, 2026-11-08

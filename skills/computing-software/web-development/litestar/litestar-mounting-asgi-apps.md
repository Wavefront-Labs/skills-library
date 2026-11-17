---
id: computing-software.web-development.litestar.litestar-mounting-asgi-apps
name: litestar-mounting-asgi-apps
category: computing-software
field: web-development
product: litestar
tags: [litestar, asgi, mount, is-mount, copy-scope, starlette, route-handlers]
level: practitioner
status: docs-checked
description: "Write raw ASGI route handlers with @asgi and mount whole ASGI apps (such as Starlette) on a sub-path in Litestar using is_mount and copy_scope."
sources: [https://docs.litestar.dev/latest/usage/routing/overview.html, https://docs.litestar.dev/latest/usage/routing/handlers.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar ASGI handlers and mounting

Goal: handle raw ASGI traffic or mount a third-party ASGI app under a sub-path.

## Method

- `@asgi(path=...)` creates an `ASGIRouteHandler`; the class can also be used directly: `ASGIRouteHandler(path="/my-asgi-app", fn=my_asgi_app)`.

```python
@asgi(path="/my-asgi-app")
async def my_asgi_app(scope: Scope, receive: Receive, send: Send) -> None:
    if scope["type"] == "http":
        if scope["method"] == "GET":
            response = Response({"hello": "world"})
            await response(scope=scope, receive=receive, send=send)
        return
    response = Response({"detail": "unsupported request"}, status_code=HTTP_400_BAD_REQUEST)
    await response(scope=scope, receive=receive, send=send)
```

- Exactly three kwargs must be defined: `scope`, `receive`, `send`. `scope` always has `type` (`http` or `websocket`) and `path`; for `http` it has `method` (DELETE, GET, POST, PATCH, PUT, HEAD).
- ASGI handler functions must be `async def`; this is enforced by inspection.
- Mount an app with `is_mount=True`; the handler receives all requests to the path and any sub path (`/some/sub-path`, `/some/sub-path/abc`, ...) but not `/some/sub-path-other`.

```python
@asgi("/some/sub-path", is_mount=True)
async def my_asgi_app(scope: "Scope", receive: "Receive", send: "Send") -> None:
    body = json.dumps({"forwarded_path": scope["path"]})
    response = ASGIResponse(body=body.encode("utf-8"))
    await response(scope, receive, send)
```

For a request to `/some/sub-path`, `scope["path"]` is `"/"`; for `/some/sub-path/abc` it is `"/abc/"`.

- Wrap a foreign app (e.g. Starlette) with `asgi(path="/some/sub-path", is_mount=True)(Starlette(routes=[...]))` and register the result in `route_handlers`.

## Gotchas

- The handler receives a copy of `scope` (mount or not), so top-level keys the wrapped app adds, replaces or removes are not seen by the outer app. The copy is shallow, so nested values like `scope["state"]` are shared.
- Pass `copy_scope=False` if the wrapped app must communicate with the outer app through the scope, e.g. writing `scope["user"]` for outer middleware.

## Verify

Request `/some/sub-path/abc` on the mount example; the JSON shows `forwarded_path` as `/abc/`.

## Checked

2026-11-07. Read the full cited page(s) (usage/routing/overview.html, usage/routing/handlers.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.

---
id: computing-software.web-development.litestar.litestar-lifecycle-hooks
name: litestar-lifecycle-hooks
category: computing-software
field: web-development
product: litestar
tags: [litestar, lifecycle-hooks, before-request, after-request, after-response, layered, request-response]
level: practitioner
status: docs-checked
description: "Run callables around the Litestar request-response cycle with before_request, after_request and after_response, and override them per layer."
sources: [https://docs.litestar.dev/latest/usage/lifecycle-hooks.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar life cycle hooks

Goal: execute a callable at a defined point of the request-response cycle.

## Method

| Hook | Runs |
|---|---|
| `before_request` | before the route handler function |
| `after_request` | after the route handler function |
| `after_response` | after the response has been sent |

- `before_request`: any callable taking a `Request` as first parameter, returning `None` or a value usable as a response. If it returns a value, the route handler for this request is bypassed.

```python
async def before_request_handler(request: Request) -> dict[str, str] | None:
    name = request.query_params["name"]
    if name == "Ben":
        return {"message": "These are not the bytes you are looking for"}
    request.state["message"] = f"Use the handler, {name}"
    return None

app = Litestar(route_handlers=[handler], before_request=before_request_handler)
```

- `after_request`: runs once the handler returned and the response object is resolved. Takes a `Response` first parameter and must return a `Response`, not necessarily the one received.

```python
async def after_request(response: Response) -> Response:
    if response.media_type == MediaType.TEXT:
        return Response({"message": response.content})
    return response

app = Litestar(route_handlers=[hello, goodbye], after_request=after_request)
```

- `after_response`: takes a `Request` first parameter and returns nothing. Meant for data post-processing, sending data to third-party services, gathering metrics.

```python
async def after_response(request: Request) -> None:
    COUNTER[request.url.path] += 1

app = Litestar(route_handlers=[hello], after_response=after_response)
```

## Layering

Hooks are part of the layered architecture: set them on app, router, controller or handler; the layer closest to the handler takes precedence. Example: `after_request=after_request_app` on `Litestar(...)` and `@get("/override", after_request=after_request_handler)` on one handler, so `/override` uses the handler hook and `/` the app hook.

## Gotchas

- `after_response` runs after the response is already returned, so state it updates (e.g. the `COUNTER` dict) is not reflected in that response.

## Verify

With the before_request example, `/?name=Luke` returns "Use the handler, Luke" from the handler, while `/?name=Ben` returns the bypass message.

## Checked

2026-11-07. Read the full cited page(s) (usage/lifecycle-hooks.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.

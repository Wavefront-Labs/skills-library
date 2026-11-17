---
id: computing-software.web-development.litestar.litestar-exception-handling
name: litestar-exception-handling
category: computing-software
field: web-development
product: litestar
tags: [litestar, exceptions, exception-handler, http-exception, validation-exception, layers, error-responses]
level: practitioner
status: docs-checked
description: "Raise Litestar HTTPException subclasses and register exception_handlers keyed by exception class or status code on app and handler layers."
sources: [https://docs.litestar.dev/latest/usage/exceptions.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar exceptions and exception handlers

Goal: return controlled error responses and override how exceptions are rendered.

## Method

`HTTPException` (subclass of `LitestarException`) serializes to JSON `{"status_code": 500, "detail": "Internal Server Error", "extra": {}}`. Pre-set subclasses: `ValidationException` 400, `NotAuthorizedException` 401, `PermissionDeniedException` 403, `NotFoundException` 404, `InternalServerException` 500, `ServiceUnavailableException` 503; `ImproperlyConfiguredException` (500) is used internally for configuration errors, and `MissingDependencyException` for missing extras.

Lookup: Litestar first looks for a user-defined handler, traversing layers from route handler up to application, then falls back to built-in handlers (for `LitestarException` and `HTTPException`). With no handler at all the exception is re-raised for the ASGI server. Built-in responses respect the handler's media type, falling back to JSON.

Custom handlers: pass `exception_handlers`, a dict mapping exception classes or status codes to callables `(request, exc) -> Response`:

```python
def plain_text_exception_handler(_: Request, exc: Exception) -> Response:
    status_code = getattr(exc, "status_code", HTTP_500_INTERNAL_SERVER_ERROR)
    detail = getattr(exc, "detail", "")
    return Response(media_type=MediaType.TEXT, content=detail, status_code=status_code)

app = Litestar(route_handlers=[index],
               exception_handlers={HTTPException: plain_text_exception_handler})
```

Granular mapping from the page:

```python
exception_handlers={
    ValidationException: validation_exception_handler,
    HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler,
    ValueError: value_error_handler,
}
```

Layers: handlers can be set on any layer and lower layers override higher ones. Example: `@get("/greet", exception_handlers={ValidationException: router_handler_exception_handler})` handles `ValidationException` only inside that handler, while the app-level `{HTTPException: app_exception_handler}` covers the rest.

## Gotchas

- Validation failures produce a `ValidationException` whose `extra` carries the validation error message, and all such messages are exposed to API consumers by default; adjust the exception contents if you do not want that.
- The router's own `404 Not Found` and `405 Method Not Allowed` are handled only by app-layer handlers, so pass those to the `Litestar` constructor.

## Verify

With the page's per-exception example, request `/validation-error` without the query param (handler text starts "validation error:"), `/server-error`, and `/value-error` ("value error: this is wrong").

## Checked

2026-11-07. Read the full cited page(s) (usage/exceptions.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.

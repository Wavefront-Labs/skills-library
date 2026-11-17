---
id: computing-software.web-development.django-ninja.django-ninja-exception-handlers
name: django-ninja-exception-handlers
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, exception-handlers, errors, httperror, http404, error-handling]
level: practitioner
status: docs-checked
description: "Raise HttpError, register custom or override default exception handlers on a NinjaAPI, customize 404s and unhandled exceptions."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/errors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: control the response returned when an exception occurs in an operation.

## Defaults
| Exception | Behavior |
|---|---|
| `ninja.errors.HttpError` | `{"detail": <message>}` with the given status |
| `ninja.errors.ValidationError` | `{"detail": <errors>}`, status 422 |
| `django.http.Http404` | `{"detail": "Not Found"}`, 404 |
| `Exception` | `DEBUG=True`: plain-text traceback, 500. Otherwise re-raised for Django's normal handling |

`AuthenticationError` (401), `AuthorizationError` (403) and `Throttled` (429) subclass `HttpError`. Ninja raises `AuthenticationError` itself; `AuthorizationError` is for you to raise.

## Raise HttpError
```python
from ninja.errors import HttpError

@api.get("/some/resource")
def some_operation(request):
    if not request.user.is_staff:
        raise HttpError(503, "Service Unavailable. Please retry later.")
    return {"message": "Hello"}
```

## Custom handler
A handler takes `(request, exc)` and must return an `HttpResponse`. `api.create_response()` builds one via the API's renderer.

```python
@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(request, {"message": "Please retry later"}, status=503)
```

`exception_handler` wraps `api.add_exception_handler(exc_class, handler)`. Lookup walks the exception's `__mro__` and uses the first registered handler, so a handler for `HttpError` also covers its subclasses unless a more specific one exists. Override a default the same way, e.g. `@api.exception_handler(AuthenticationError)`.

## 404 for undefined URLs
`@api.exception_handler(Http404)` only covers `Http404` raised inside a Ninja operation (e.g. `get_object_or_404`). Undefined URLs never reach Ninja; set Django's `handler404 = "myapp.views.custom_404"` in the root `urls.py`. It takes `request` and `exception`, and is used only when `DEBUG=False`.

## Catch-all
```python
@api.exception_handler(Exception)
def catch_all(request, exc: Exception):
    logger.exception(exc)
    return api.create_response(request, {"detail": "Internal server error"}, status=500)
```
Overriding `Exception` swallows unanticipated errors, so keep logging.

## Gotcha
Handlers live on the `NinjaAPI` instance; `Router` has no `exception_handler`. Each `NinjaAPI` instance needs its own registrations.

## Checked

2026-11-07: Confirmed against guide/errors.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.

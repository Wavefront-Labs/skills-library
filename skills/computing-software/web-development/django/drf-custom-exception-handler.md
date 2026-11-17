---
id: computing-software.web-development.django.drf-custom-exception-handler
name: drf-custom-exception-handler
category: computing-software
field: web-development
product: django
tags: [drf-exception-handler, api-error-format, problem-details, django-rest-framework, django]
level: practitioner
status: verified
description: "A consistent DRF error format: writing a custom EXCEPTION_HANDLER, mapping Django and domain exceptions, field errors, RFC 9457 problem details, logging and not leaking internals."
sources:
  - https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling
  - https://www.rfc-editor.org/rfc/rfc9457
  - https://github.com/ghazi-git/drf-standardized-errors
  - https://www.rfc-editor.org/rfc/rfc9457
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DRF custom exception handler and error format

DRF's default errors vary in shape: `{"detail": "..."}` for most, `{"field": ["msg"]}` for validation, and unhandled exceptions become HTML 500s. Clients want one shape.

## 1. Handler
```python
# core/api/exceptions.py
from rest_framework.views import exception_handler
from rest_framework import exceptions, status
from rest_framework.response import Response
import logging
log = logging.getLogger(__name__)

class DomainError(Exception):
    status_code = 409; code = "conflict"

def api_exception_handler(exc, context):
    if isinstance(exc, DomainError):
        exc = exceptions.APIException(detail=str(exc), code=DomainError.code); exc.status_code = DomainError.status_code
    response = exception_handler(exc, context)          # handles APIException, Http404, PermissionDenied
    if response is None:                                # unhandled -> 500 JSON, log with traceback
        log.exception("Unhandled API error", extra={"view": context["view"].__class__.__name__})
        return Response({"type": "about:blank", "title": "Internal Server Error", "status": 500},
                        status=500, content_type="application/problem+json")
    body = {"type": "about:blank", "title": response.status_text, "status": response.status_code}
    if isinstance(exc, exceptions.ValidationError):
        body["title"] = "Validation failed"; body["errors"] = response.data
    else:
        detail = response.data.get("detail") if isinstance(response.data, dict) else response.data
        body["detail"] = detail
        body["code"] = getattr(detail, "code", None)     # ErrorDetail.code: "conflict", "not_found", "throttled"...
    response.data = body
    response.content_type = "application/problem+json"   # setting the header is not enough: the renderer overwrites it
    return response

# settings
REST_FRAMEWORK = {"EXCEPTION_HANDLER": "core.api.exceptions.api_exception_handler"}
```
- Preserve headers DRF sets (`WWW-Authenticate` for 401, `Retry-After` for throttling) - the default handler adds them to `response`.
- Django's `ValidationError` raised in model `clean()`/`save()` isn't converted automatically (`exception_handler` returns `None`, so it reaches the 500 branch above); convert to DRF `ValidationError` in serializers. Django `Http404` and `PermissionDenied` are handled (404 / 403).

## 2. Format choice
RFC 9457 problem details (`type`, `title`, `status`, `detail`, `instance`, plus extensions like `errors`) is a standard clients and gateways understand. `drf-standardized-errors` provides a ready-made, documented format with drf-spectacular schema support.

## 3. Rules
- Never return tracebacks, SQL or internal exception messages in production responses.
- Stable machine-readable `code`s (`"insufficient_funds"`) for clients to branch on; human `detail` can change.
- Log 5xx with request id; 4xx at info/warning level only.
- Document error responses in the OpenAPI schema.

## Verify
- [ ] 400, 401, 403, 404, 409, 429 and 500 all return the same JSON shape with correct status and content type; unhandled exceptions logged with traceback but not exposed.

## Checked
Django 6.1.2, DRF 3.18.3, drf-spectacular 0.30.0 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets. The first version of the handler was run as written before fixing.
- Found by running: `exc.default_code` is `"error"` for the converted `DomainError` (the response had `"code": "error"`, never `"conflict"`) and `None` for `Http404`; reading `ErrorDetail.code` from `response.data["detail"]` gives `conflict`, `not_found`, `throttled`, `not_authenticated`.
- Found by running: `response["Content-Type"] = ...` is overwritten when the response renders (400, 403, 404, 409 and 429 came back as `application/json`); only the 500 branch (which passes `content_type=` to `Response`) was `application/problem+json`. Setting `response.content_type` works (tested, header read back `application/problem+json`).
- Run: 400 validation (`errors` carries the serializer errors), 403 with `not_authenticated`, 404, 409, 429 with the `Retry-After: 60` header kept, 500 JSON for an unhandled `RuntimeError`; a `BasicAuthentication` view returned 401 with `WWW-Authenticate: Basic realm="api"`.
- Fetched: RFC 9457 (Problem Details, obsoletes RFC 7807) from rfc-editor.org. `drf-standardized-errors` 0.16.0 exists on PyPI.

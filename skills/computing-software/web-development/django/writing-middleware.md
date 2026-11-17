---
id: computing-software.web-development.django.writing-middleware
name: writing-middleware
category: computing-software
field: web-development
product: django
tags: [django, django-middleware, request-response, process-view, async-middleware, python, web-development]
level: practitioner
status: verified
description: "Writing Django middleware: the callable pattern, ordering in MIDDLEWARE, process_view/process_exception hooks, sync and async support and performance cautions."
sources:
  - https://docs.djangoproject.com/en/stable/topics/http/middleware/
  - https://docs.djangoproject.com/en/stable/ref/middleware/
  - https://docs.djangoproject.com/en/stable/topics/async/#async-views
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing middleware

**Goal:** cross-cutting request/response logic (request ids, timing, tenant resolution, headers) placed at the right point of the chain.

## 1. The pattern
```python
# core/middleware.py
import time, uuid, logging
log = logging.getLogger(__name__)

class RequestIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response          # one-time setup at server start
    def __call__(self, request):
        request.id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        start = time.perf_counter()
        response = self.get_response(request)     # everything below in the chain + the view
        response["X-Request-ID"] = request.id
        log.info("request", extra={"id": request.id, "path": request.path, "ms": (time.perf_counter() - start) * 1000})
        return response
```
```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "core.middleware.RequestIdMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    ...
]
```

## 2. Ordering
Requests go top -> bottom, responses bottom -> top. Rules (Django middleware docs, "Middleware ordering"): `SecurityMiddleware` near the top (docs: mainly when SSL redirect is on, to skip other middleware); `SessionMiddleware` before `AuthenticationMiddleware` (needs session) before anything using `request.user`; `CsrfViewMiddleware` before views that assume CSRF checks; `GZipMiddleware` before any middleware that may change or use the response body. Returning a response early (short-circuit) skips everything below.

## 3. Optional hooks
- `process_view(request, view_func, view_args, view_kwargs)` - runs after URL resolution; good for per-view decisions (e.g. check a decorator attribute).
- `process_exception(request, exception)` - return a response to handle, or `None` to continue.
- `process_template_response(request, response)` - modify `TemplateResponse` context before render.

## 4. Async compatibility
Django adapts sync middleware under ASGI with a thread switch per request. For async stacks make it dual-mode:
```python
from asgiref.sync import iscoroutinefunction, markcoroutinefunction
class TimingMiddleware:
    sync_capable = True; async_capable = True
    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(get_response): markcoroutinefunction(self)
    def __call__(self, request):
        if iscoroutinefunction(self):
            return self.__acall__(request)
        return self.get_response(request)
    async def __acall__(self, request):
        return await self.get_response(request)
```

## 5. Cautions
- Runs on every request including static/media in dev and health checks: keep it cheap; no DB queries unless required.
- Don't read `request.body` for large uploads; it buffers everything.
- Streaming responses (`StreamingHttpResponse`) have no `.content`; check `response.streaming`.
- Raising `MiddlewareNotUsed` in `__init__` disables it (feature flags; run, logged at DEBUG as "MiddlewareNotUsed: '<path>'").

## Verify
- [ ] Response headers include the request id; logs share it.
- [ ] Unit test with `RequestFactory` + a dummy `get_response`.
- [ ] Under ASGI, no "Synchronous handler adapted for middleware ..." / "Asynchronous handler adapted for middleware ..." messages on the `django.request` logger at DEBUG for hot paths (exact wording seen on Django 6.1.2; the sync-only class and the dual-mode class were both run under `AsyncClient`).

---
id: computing-software.web-development.django-ninja.django-ninja-temporal-response
name: django-ninja-temporal-response
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, temporal-response, response-headers, cookies, httpresponse, status-code]
level: practitioner
status: docs-checked
description: "Set response headers, cookies and status from a Django Ninja view via an HttpResponse-typed argument, and customize create_temporal_response."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/temporal-response.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Headers, cookies and status on the response

Declare a parameter annotated `HttpResponse`; Ninja passes a response object to modify. It is matched by **type**, not name, and works in async views.

```python
from django.http import HttpResponse

@api.get("/cookie")
def feed_cookiemonster(request, response: HttpResponse):
    response.set_cookie("cookie", "delicious")
    response["X-Cookiemonster"] = "blue"
    return {"cookiemonster_happy": True}
```

Still return your normal data; the object is for headers, cookies and status, not the body.

## Headers and cookies

Assign like a dict: `response["X-Total-Count"] = 42`. Cookies use Django's own `set_cookie()` / `delete_cookie()`, so all arguments work (`max_age`, `expires`, `path`, `domain`, `secure`, `httponly`, `samesite`):

```python
response.set_cookie("session_id", "abc123", max_age=3600,
                    secure=True, httponly=True, samesite="Lax")
response.delete_cookie("session_id")
```

## Status code gotcha

Setting `response.status_code = 201` and returning a plain dict does **not** stick: Ninja computes the status from the return value (200 by default) and overwrites it after your view returns. Return a `Status` instead:

```python
@api.post("/items", response={200: dict, 201: dict})
def create_item(request, response: HttpResponse):
    response["Location"] = "/items/1"
    return Status(201, {"id": 1, "created": True})
```

Headers and cookies are preserved either way. Returning the `response` object itself always works since any `HttpResponse` is returned as-is.

## Limits

The object is created per request by `NinjaAPI.create_temporal_response()`, initially with only a `Content-Type` matching the renderer. Built-in error responses (404, 422, `HttpError`, default exception handler) do not inherit headers or cookies you set; set them in a custom exception handler.

## Customize the base

```python
class MyAPI(NinjaAPI):
    def create_temporal_response(self, request):
        response = super().create_temporal_response(request)
        response["X-Powered-By"] = "Django Ninja"
        return response

api = MyAPI()
```

## Checked

2026-11-08: Read django-ninja docs/docs/guide/temporal-response.md from GitHub. Confirmed against the whole page: HttpResponse parameter matched by type, header and cookie examples, the status code overwrite and Status workaround, create_temporal_response and the error response limitation. Nothing removed.

Method: documentation only; no commands were run.

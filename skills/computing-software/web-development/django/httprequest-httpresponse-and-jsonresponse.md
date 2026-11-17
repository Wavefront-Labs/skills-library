---
id: computing-software.web-development.django.httprequest-httpresponse-and-jsonresponse
name: httprequest-httpresponse-and-jsonresponse
category: computing-software
field: web-development
product: django
tags: [httprequest, jsonresponse, httpresponse, django-views, django]
level: intro
status: verified
description: "Django request and response objects: GET/POST/body parsing, headers and META, JsonResponse and the safe flag, status codes, redirects, cookies and files."
sources:
  - https://docs.djangoproject.com/en/stable/ref/request-response/
  - https://docs.djangoproject.com/en/stable/topics/http/shortcuts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HttpRequest, HttpResponse and JsonResponse

## 1. Reading the request
```python
def search(request):
    q = request.GET.get("q", "").strip()            # QueryDict; getlist("tag") for repeated keys
    page = int(request.GET.get("page", 1))
    if request.method == "POST":
        name = request.POST["name"]                 # form-encoded or multipart only
        upload = request.FILES.get("avatar")
    data = json.loads(request.body or b"{}")         # JSON bodies are NOT in request.POST
    token = request.headers.get("Authorization")    # case-insensitive
    ip = request.META.get("REMOTE_ADDR")            # behind a proxy, trust X-Forwarded-For only from your proxy
    user = request.user                              # AnonymousUser if not logged in
```
- `request.body` can only be read before `request.POST`/streaming reads: reading `request.POST` first and then `request.body` raises `RawPostDataException` (urlencoded and multipart both); `request.body` first and then `request.POST` works. Size capped by `DATA_UPLOAD_MAX_MEMORY_SIZE`.
- `request.build_absolute_uri()` and `request.get_host()` depend on `ALLOWED_HOSTS` and `USE_X_FORWARDED_HOST`.
- `request.htmx` style helpers come from packages; plain Django: `request.headers.get("HX-Request")`.

## 2. Responses
```python
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, Http404
from django.shortcuts import redirect, get_object_or_404

return HttpResponse("Created", status=201, content_type="text/plain")
return JsonResponse({"results": rows, "count": n})
return JsonResponse(items_list, safe=False)             # top-level list needs safe=False (otherwise TypeError)
return JsonResponse({"error": "invalid"}, status=422)
return redirect("order-detail", pk=order.pk)            # 302; permanent=True for 301
raise Http404("No such order")                          # renders 404 template
```
- `JsonResponse` uses `DjangoJSONEncoder` (handles datetime, Decimal, UUID); pass `encoder=` for custom types and `json_dumps_params={"ensure_ascii": False}` for readable Unicode.
- Set headers like a dict: `resp["Cache-Control"] = "no-store"`; `resp.headers` in modern Django.
- Cookies: `resp.set_cookie("theme", "dark", max_age=31536000, secure=True, httponly=True, samesite="Lax")`; signed: `set_signed_cookie`.

## 3. Status code helpers
`HttpResponseBadRequest` (400), `HttpResponseForbidden` (403), `HttpResponseNotFound` (404), `HttpResponseNotAllowed(["GET"])` (405), `HttpResponseGone` (410). For APIs with many endpoints, DRF's `Response` and exception handling are cleaner.

## 4. Streaming and files
`StreamingHttpResponse(generator)` for large CSV exports; `FileResponse(open(path, "rb"), as_attachment=True, filename="report.pdf")` for files.

## Verify
- [ ] JSON endpoints parse `request.body`, return correct status codes and handle invalid JSON with 400; client IPs taken from a trusted proxy header only.

## Checked
Django 6.1.2, DRF 3.18.3 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: `GET` params (`q` stripped, `getlist("tag")`), `Authorization` header, `REMOTE_ADDR`, `build_absolute_uri`, form POST `request.POST["name"]`, JSON body not in `request.POST` but in `json.loads(request.body)`.
- Run: `RawPostDataException` for `.body` after `.POST` (urlencoded and multipart); `JsonResponse([1, 2])` -> TypeError, `safe=False` -> `[1, 2]`; `JsonResponse` encoded datetime, Decimal and UUID and honoured `json_dumps_params={"ensure_ascii": False}`.
- Run: `Cache-Control` header, `resp.headers[...]`, `set_cookie(..., secure=True, httponly=True, samesite="Lax")`, `set_signed_cookie`, `redirect()` 302 and `permanent=True` 301, `Http404("No such order")`, `HttpResponseNotAllowed(["GET"])` = 405, `HttpResponseGone` = 410, `FileResponse(open(...), as_attachment=True, filename="report.pdf")` header `attachment; filename="report.pdf"`.
- Installed: django-htmx 1.29.0 (the `request.htmx` helper the skill mentions).

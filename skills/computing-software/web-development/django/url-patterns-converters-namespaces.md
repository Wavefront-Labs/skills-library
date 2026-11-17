---
id: computing-software.web-development.django.url-patterns-converters-namespaces
name: url-patterns-converters-namespaces
category: computing-software
field: web-development
product: django
tags: [django, path-converters, url-reverse, url-namespaces, include, urlconf, reverse-lazy, python, web-development, url-dispatcher, django-views]
level: practitioner
status: verified
description: "Designing Django URLconfs: path converters and custom converters, include() and app/instance namespaces, reverse/reverse_lazy and {% url %} usage."
sources:
  - https://docs.djangoproject.com/en/stable/topics/http/urls/
  - https://docs.djangoproject.com/en/stable/ref/urlresolvers/
  - https://docs.djangoproject.com/en/stable/ref/urls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# URL patterns: converters, include, namespaces, reverse

**Goal:** URLs defined once, never hard-coded, with typed parameters.

## 1. path and converters
```python
# shop/urls.py
from django.urls import path, register_converter
from . import views
app_name = "shop"                                     # application namespace
urlpatterns = [
    path("", views.index, name="index"),
    path("products/<int:pk>/", views.detail, name="detail"),
    path("products/<slug:slug>/", views.by_slug, name="by_slug"),
    path("files/<path:subpath>", views.file, name="file"),
]
```
Built-ins: `str` (no `/`), `int`, `slug`, `uuid`, `path` (includes `/`). Converted values arrive typed (`pk` is an `int`). `re_path` for legacy regexes.

## 2. Custom converter
```python
class YearConverter:
    regex = r"[0-9]{4}"
    def to_python(self, value): return int(value)
    def to_url(self, value): return f"{value:04d}"
register_converter(YearConverter, "yyyy")
path("archive/<yyyy:year>/", views.archive, name="archive")
```
Raise `ValueError` in `to_python` to make that pattern not match: resolution moves on to the next pattern (run: a later `<str:x>` pattern answered) and gives 404 only if nothing else matches.

## 3. include and namespaces
```python
# project/urls.py
urlpatterns = [
    path("shop/", include("shop.urls")),                                   # uses app_name "shop"
    path("api/v1/", include(("api.urls", "api"), namespace="api-v1")),     # instance namespace
    path("admin/", admin.site.urls),
]
```
Reverse with `namespace:name`: `reverse("shop:detail", args=[42])`, `reverse("api-v1:orders")`. Instance namespaces let the same app be mounted twice.

## 4. Reversing
```python
from django.urls import reverse, reverse_lazy
return redirect("shop:detail", pk=obj.pk)            # redirect() reverses names
success_url = reverse_lazy("shop:index")             # class attributes / module level: lazy
```
```django
<a href="{% url 'shop:detail' product.pk %}">...</a>
```
Models: `def get_absolute_url(self): return reverse("shop:detail", kwargs={"pk": self.pk})` - used by admin "View on site" and generic views.

## 5. Ordering and trailing slashes
Patterns match top-down; put specific before generic (`products/new/` before `products/<slug:slug>/`). `APPEND_SLASH=True` redirects `/x` to `/x/` for GETs only (a POST to the slashless URL raises `RuntimeError: You called this URL via POST, but the URL doesn't end in a slash` in DEBUG, run on Django 6.1.2; the GET redirect was a 301).

## 6. Debug
`python manage.py show_urls` (the django-extensions package, not Django core) lists all routes; `resolve("/shop/products/1/")` in a shell shows which view matched.

## Verify
- [ ] `grep -rn 'href="/' templates` - no hard-coded internal URLs.
- [ ] `reverse()` for every named URL works in a smoke test.
- [ ] Ambiguous patterns (slug vs fixed word) resolve to the intended view.

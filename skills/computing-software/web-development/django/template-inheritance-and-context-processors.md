---
id: computing-software.web-development.django.template-inheritance-and-context-processors
name: template-inheritance-and-context-processors
category: computing-software
field: web-development
product: django
tags: [django, template-inheritance, context-processors, django-templates, include, block-super, python, web-development]
level: practitioner
status: verified
description: "Structuring Django templates: base templates and blocks, block.super, include with only, template directories and loaders, and writing lean context processors."
sources:
  - https://docs.djangoproject.com/en/stable/ref/templates/language/#template-inheritance
  - https://docs.djangoproject.com/en/stable/ref/templates/builtins/
  - https://docs.djangoproject.com/en/stable/ref/templates/api/#writing-your-own-context-processors
  - https://docs.djangoproject.com/en/stable/topics/templates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template inheritance, includes and context processors

**Goal:** one base layout, small reusable partials, and global template data without per-view boilerplate.

## 1. Three-level inheritance
```django
{# templates/base.html #}
<!doctype html><html lang="{{ LANGUAGE_CODE }}">
<head><title>{% block title %}Acme{% endblock %}</title>{% block extra_head %}{% endblock %}</head>
<body>{% include "partials/nav.html" %}<main>{% block content %}{% endblock %}</main></body></html>

{# templates/shop/base_shop.html #}
{% extends "base.html" %}
{% block title %}Shop | {{ block.super }}{% endblock %}

{# templates/shop/product_detail.html #}
{% extends "shop/base_shop.html" %}
{% block content %}<h1>{{ product.name }}</h1>{% endblock %}
```
- `{% extends %}` must be the first template tag (plain text may precede it; the Django docs wording).
- `{{ block.super }}` appends to the parent's block instead of replacing it.
- Content outside blocks in a child template is ignored.

## 2. include
```django
{% include "partials/card.html" with item=product only %}
{% for p in products %}{% include "partials/card.html" with item=p %}{% endfor %}
```
`only` passes just the listed variables - makes partials explicit and safer. Includes in loops are fine; cached loaders make them cheap.

## 3. Directories and loaders
```python
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],          # project-level overrides
    "APP_DIRS": True,                          # app/templates/
    "OPTIONS": {"context_processors": [...]},
}]
```
Namespace app templates: `shop/templates/shop/detail.html` so apps don't collide. The cached loader is enabled automatically when `DEBUG=False` and `OPTIONS["loaders"]` is not set (measured: the engine's loader was the cached `Loader` wrapping the filesystem and app-directories loaders).

## 4. Context processors
```python
# core/context_processors.py
def site(request):
    return {"SITE_NAME": settings.SITE_NAME, "SUPPORT_EMAIL": settings.SUPPORT_EMAIL}
```
Add `"core.context_processors.site"` to `context_processors`. They run for **every** template rendered with a `RequestContext` (`render()`): no DB queries unless lazy (`SimpleLazyObject`) or cached. Built-ins worth knowing: `request`, `auth` (`user`, `perms`), `messages`, `csrf` (always on), `i18n`.

## 5. Keep logic out
Templates can't call methods with arguments - compute in the view or a custom tag. Avoid N+1 hidden in templates (`{{ order.customer.name }}` in loops) by `select_related` in the view.

## Verify
- [ ] Every page extends the base and sets a title block.
- [ ] Debug toolbar: context processors add no queries per request.
- [ ] Partials included with `only` render without missing-variable surprises.

## Checked
Django 6.1.2, DRF 3.18.3 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: three-level inheritance (`base.html` -> `shop/base_shop.html` -> page): the title rendered `Shop | Acme` using `{{ block.super }}`, text outside blocks in the child (`OUTSIDE-BLOCK-IGNORED`) did not appear, `{% include ... with item="A" only %}` rendered `CARD[A]`, `{{ LANGUAGE_CODE }}` in the `<html lang>` attribute rendered `en-us` with the `i18n` context processor enabled.
- Run: with DEBUG off the template engine's loaders are the cached `Loader` over the filesystem and app-directories loaders.
- Run: the `request`, `auth` (`user`), `messages` and `i18n` context processors supplied variables to `render()`; the 404 template got `user` as a RequestContext variable, 500 got none.

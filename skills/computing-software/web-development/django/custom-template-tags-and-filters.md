---
id: computing-software.web-development.django.custom-template-tags-and-filters
name: custom-template-tags-and-filters
category: computing-software
field: web-development
product: django
tags: [django, custom-template-tags, template-filters, simple-tag, inclusion-tag, templatetags, python, web-development]
level: practitioner
status: verified
description: "Writing Django custom template filters and tags: templatetags package layout, simple_tag, inclusion_tag, takes_context, autoescape and mark_safe safety."
sources:
  - https://docs.djangoproject.com/en/stable/howto/custom-template-tags/
  - https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.html.format_html
  - https://docs.djangoproject.com/en/stable/ref/templates/builtins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom template tags and filters

**Goal:** presentation helpers reusable across templates without opening XSS holes.

## 1. Layout
```
shop/
  templatetags/
    __init__.py
    shop_tags.py
```
The app must be in `INSTALLED_APPS`; restart the dev server after creating the module (the `templatetags` package needs its `__init__.py`). Load with `{% load shop_tags %}`.

## 2. Filters
```python
from django import template
register = template.Library()

@register.filter
def cents(value):
    """{{ order.total_cents|cents }} -> 12.34"""
    try: return f"{int(value) / 100:.2f}"
    except (TypeError, ValueError): return ""
```
Filters take one value and at most one argument (`{{ x|truncate:20 }}`; a second argument is a `TemplateSyntaxError`). Filters should never raise: Django does not swallow the exception (a filter doing `1/0` makes the whole render raise `ZeroDivisionError`), so catch bad input and return `""`.

## 3. simple_tag
```python
@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    """<a href="?{% query_transform page=3 %}"> keeps other GET params"""
    q = context["request"].GET.copy()
    for k, v in kwargs.items(): q[k] = v
    return q.urlencode()
```
`{% query_transform page=3 as qs %}` stores the result in a variable. Output is auto-escaped unless marked safe (so `&` in the query string renders as `&amp;`, which is correct inside an `href`). Literal strings written in the template are treated as safe: `{% link 'u' '<i>' %}` is not escaped by `format_html`, a variable holding `<script>` is.

## 4. inclusion_tag
```python
@register.inclusion_tag("shop/partials/cart_badge.html", takes_context=True)
def cart_badge(context):
    return {"count": context["request"].session.get("cart_count", 0)}
```
Renders a template with its own context - good for widgets used on many pages.

## 5. Escaping rules
- Build HTML with `format_html("<a href='{}'>{}</a>", url, label)` - it escapes arguments.
- `mark_safe` only on strings you fully control; never on user input.
- Filters that return HTML: `@register.filter(is_safe=True, needs_autoescape=True)` and escape input with `conditional_escape` when `autoescape` is on.

## 6. Performance
Tags run per render; avoid DB queries in tags used inside loops. Cache expensive results or move to the view.

## Verify
- [ ] Unit tests render `Template("{% load shop_tags %}{{ 1234|cents }}").render(Context())`.
- [ ] Passing `<script>` through every custom tag/filter renders escaped.
- [ ] No `mark_safe` on values derived from users (`grep -rn mark_safe`).

## Checked
Django 6.1.2, DRF 3.18.3, drf-spectacular 0.30.0 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: `cents` filter (`1234|cents` -> `12.34`, bad input -> empty string); two-argument filter -> TemplateSyntaxError; a raising filter -> ZeroDivisionError from `render()`.
- Run: `query_transform` with `takes_context` on `?a=1&page=2` gave `a=1&amp;page=3`, and the `as qs` form stored it; `inclusion_tag` rendered the partial with `count` from the session (`BADGE 4`).
- Run: `format_html` / `simple_tag` / `bold` (`is_safe=True, needs_autoescape=True`, using `conditional_escape`) escaped a variable `<script>` to `&lt;script&gt;`; template string literals were not escaped.
- Run: template inheritance rendering of a page using the tags (product name `<b>Chair</b>` auto-escaped in `{ }`).

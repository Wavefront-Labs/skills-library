---
id: computing-software.web-development.django.autoescaping-mark-safe-and-filters
name: autoescaping-mark-safe-and-filters
category: computing-software
field: web-development
product: django
tags: [django-autoescape, mark-safe, template-filters, xss-prevention, django]
level: practitioner
status: verified
description: "How Django template autoescaping protects against XSS: what is escaped, safe and escapejs filters, mark_safe and format_html, json_script for data, and common unsafe patterns."
sources:
  - https://docs.djangoproject.com/en/stable/ref/templates/language/#automatic-html-escaping
  - https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.html.format_html
  - https://docs.djangoproject.com/en/stable/ref/templates/builtins/#json-script
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autoescaping, mark_safe and built-in filters

## 1. Default behaviour
Every `{{ variable }}` is HTML-escaped: `< > ' " &` become entities. This prevents XSS in **HTML element and quoted attribute contexts**.

Not protected:
- Unquoted attributes: `<div class={{ cls }}>` - always quote.
- URLs: `<a href="{{ url }}">` escapes HTML but allows `javascript:` URLs - validate schemes server-side.
- Inline JavaScript and `<script>` blocks: HTML escaping is the wrong encoding.
- CSS contexts.

## 2. Passing data to JavaScript
```django
{{ chart_data|json_script:"chart-data" }}
<script>const data = JSON.parse(document.getElementById("chart-data").textContent);</script>
```
`json_script` safely escapes `<`, `>` and `&` for embedding (Django 6.1.2 output: `</script><&>`). Avoid `var x = "{{ value|escapejs }}"` except for simple strings; never `{{ value|safe }}` inside script.

## 3. Marking content safe
```python
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

format_html('<a href="{}">{}</a>', url, user.name)          # escapes arguments, keeps the template
format_html_join("\n", "<li>{}</li>", ((t,) for t in tags))
mark_safe(sanitized_html)                                     # only after sanitising (nh3/bleach)
```
- `mark_safe(f"<b>{user_input}</b>")` is an XSS bug: the f-string interpolates unescaped input. Use `format_html`.
- `|safe` in templates and `{% autoescape off %}` should be rare and reviewed; grep for them in code review.
- User-submitted rich text: sanitise with `nh3` (bleach's README says "no longer maintained" as of 2026-06-05 and the repo is archived) on save or render, then mark safe.

## 4. Useful filters
`escape` (force), `force_escape`, `striptags` (not a sanitiser: `<b onclick=x>hi</b><script>alert(1)</script>` becomes `hialert(1)`), `linebreaks`/`linebreaksbr` (escape then add `<p>`/`<br>`), `urlize` (escapes, adds links with `rel="nofollow"`), `truncatewords_html`, `iriencode`, `urlencode` for query parameters.

## 5. Custom filters
If a filter returns HTML, set `is_safe=True` only when the output is safe for any safe input, or use `needs_autoescape=True` and escape inputs with `conditional_escape`.

## Verify
- [ ] No `mark_safe` on interpolated strings; `|safe`/`autoescape off` usages reviewed and justified; JS data passed via json_script; URLs from users validated for scheme.

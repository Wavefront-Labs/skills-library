---
id: computing-software.web-development.django.django-with-htmx-partials
name: django-with-htmx-partials
category: computing-software
field: web-development
product: django
tags: [django, htmx, django-htmx, partial-templates, hypermedia, hx-request, python, web-development]
level: practitioner
status: docs-checked
description: "Building interactive Django pages with htmx: partial responses, django-htmx request helpers, CSRF headers, out-of-band swaps, redirects and template partials."
sources:
  - https://htmx.org/docs/
  - https://django-htmx.readthedocs.io/
  - https://github.com/carltongibson/django-template-partials
  - https://htmx.org/reference/#response_headers
  - https://htmx.org/docs/whats-new-in-htmx-4/
  - https://docs.djangoproject.com/en/stable/ref/templates/builtins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Django with htmx partials

**Goal:** server-rendered interactivity (inline edit, live search, infinite scroll) with Django templates and no SPA.

## 1. Setup
```bash
pip install django-htmx
```
```python
INSTALLED_APPS += ["django_htmx"]
MIDDLEWARE += ["django_htmx.middleware.HtmxMiddleware"]    # adds request.htmx
```
Load htmx in the base template (`<script src="{% static 'htmx.min.js' %}" defer></script>`).

## 2. CSRF for non-GET requests
```django
<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
```
Then `hx-post`/`hx-delete` pass `CsrfViewMiddleware` without a form token. In htmx 4 attributes only inherit with the `:inherited` modifier, so write `hx-headers:inherited` on the body.

## 3. Same view, full page or fragment
```python
def contact_list(request):
    contacts = Contact.objects.filter(owner=request.user, name__icontains=request.GET.get("q", ""))[:50]
    template = "contacts/_rows.html" if request.htmx else "contacts/list.html"
    return render(request, template, {"contacts": contacts})
```
```django
<input type="search" name="q" hx-get="{% url 'contacts:list' %}" hx-trigger="input changed delay:300ms, search"
       hx-target="#rows" hx-push-url="true">
<tbody id="rows">{% include "contacts/_rows.html" %}</tbody>
```
Full page reload of the pushed URL still works because the view renders the whole page for non-htmx requests. Add `Vary: HX-Request` (django-htmx's docs use `@vary_on_headers("HX-Request")`) so caches don't mix full and partial responses; htmx 4 changed some request headers (for example it adds `HX-Request-Type`), so check which header your htmx version sends.

## 4. Template partials instead of many files
With `django-template-partials` (built into Django 6.0 as `{% partialdef %}`):
```django
{% partialdef row inline %}<tr id="c-{{ c.pk }}">...</tr>{% endpartialdef %}
```
`render(request, "contacts/list.html#row", {...})` renders just that partial.

## 5. Responses that steer the client
```python
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event
return HttpResponseClientRedirect(reverse("contacts:list"))   # sends the HX-Redirect header
response = render(request, "contacts/_row.html", {"c": c})
return trigger_client_event(response, "contactSaved", {"id": c.pk})   # HX-Trigger
```
Out-of-band swaps update other regions: include `<span id="count" hx-swap-oob="true">{{ total }}</span>` in the response.

## 6. Validation errors
In htmx 2.x, 4xx and 5xx responses are not swapped by default, so return the form partial with errors and status 200, or configure `htmx.config.responseHandling` to swap 422. htmx 4.0.0 (released 2026-08-28) swaps every response except 204 and 304, removes `responseHandling` (use `htmx.config.noSwap` or `hx-status`) and makes attribute inheritance explicit.

## 7. Security and a11y
Partials are normal views: apply the same `login_required` and object scoping. Add `aria-live` to regions updated without navigation; keep links real `<a href>` with `hx-boost` for progressive enhancement.

## Verify
- [ ] Each htmx endpoint returns the full page when loaded directly.
- [ ] POST/DELETE from htmx works with CSRF enabled.
- [ ] Back/forward after `hx-push-url` restore the right state.

## Checked
Date: 2026-10-25. Documentation: htmx docs source (bigskysoftware/htmx master, 2.x docs, and the "What's New in htmx 4" page at tag v4.0.0), django-htmx docs source (adamchainz/django-htmx main), Django 6.0 release notes and template builtins.
Confirmed: `django_htmx` app and `HtmxMiddleware` with `request.htmx`, `HttpResponseClientRedirect`, `trigger_client_event`, `hx-headers` for CSRF tokens, `hx-swap-oob`, the `hx-trigger` delay syntax, `Vary: HX-Request` guidance, `{% partialdef %}` with `inline` and `template#partial` rendering (Django 6.0), htmx 2.x response-handling defaults.
Corrected or removed: the invented `django_htmx.http` Vary helper, the unsupported explanation of the HX-Redirect response, and the htmx 2-only error-swapping and inheritance statements, which now state the htmx 4 differences.
Method: documentation only; no commands were run.

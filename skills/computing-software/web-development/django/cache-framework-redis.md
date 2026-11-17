---
id: computing-software.web-development.django.cache-framework-redis
name: cache-framework-redis
category: computing-software
field: web-development
product: django
tags: [django, django-cache, redis-cache, cache-page, low-level-cache, template-fragment-caching, python, web-development]
level: practitioner
status: docs-checked
description: "Using Django's cache framework: Redis backend config, per-view and fragment caching, low-level get_or_set, key versioning, invalidation and stampede avoidance."
sources:
  - https://docs.djangoproject.com/en/stable/topics/cache/
  - https://docs.djangoproject.com/en/stable/ref/settings/#caches
  - https://docs.djangoproject.com/en/stable/topics/cache/#the-low-level-cache-api
  - https://github.com/jazzband/django-redis
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cache framework (per-view, fragment, low-level, Redis)

**Goal:** cut repeated expensive work with caches that invalidate correctly and never leak one user's data to another.

## 1. Backend
```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",     # built in since 4.0
        "LOCATION": env("REDIS_URL"),
        "TIMEOUT": 300,
        "KEY_PREFIX": "shop",
    }
}
```
`LocMemCache` is per-process (fine for dev/tests, inconsistent with multiple workers). `django-redis` is a third-party backend that adds extras such as compression (see its README). Use a separate Redis DB/instance from Celery and sessions if eviction policies differ.

## 2. Low-level API (most useful)
```python
from django.core.cache import cache
def top_products():
    return cache.get_or_set("top_products:v2", lambda: list(Product.objects.top()[:10]), timeout=600)

def on_product_change(product):
    cache.delete("top_products:v2")
```
- Cache plain data (lists/dicts), not querysets (they're lazy) - wrap in `list()`.
- Version keys by changing a suffix or `cache.incr_version`, rather than flushing.
- `cache.get_many/set_many` to batch; `cache.add` sets only if absent (simple locks).
- Async variants are prefixed with `a` (for example `aset`, `ahas_key`) and exist for all base cache methods; Django's docs say truly asynchronous cache backends are not yet supported.

## 3. Per-view caching
```python
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
@cache_page(60 * 15)
def pricing(request): ...
```
Keyed off the URL (each URL is cached separately) and the response `Vary` headers. Danger: pages that show user-specific content get cached for everyone unless they vary on cookie - and varying on cookie destroys hit rate. Use only for anonymous/public pages. Site-wide `UpdateCacheMiddleware`/`FetchFromCacheMiddleware` has the same caveats.

## 4. Template fragment caching
```django
{% load cache %}
{% cache 600 sidebar request.LANGUAGE_CODE %}...expensive sidebar...{% endcache %}
```
Extra args form part of the key - include anything the fragment varies by (user id, language). Invalidate with `make_template_fragment_key("sidebar", [lang])`.

## 5. Stampedes
When a hot key expires, many workers recompute at once. Mitigate: jittered timeouts, a lock with `cache.add("lock:key", 1, 30)`, or background refresh (Celery beat) writing ahead of expiry.

## 6. Cache headers
For CDN/browser caching use `cache_control(max_age=..., public=True)` / `never_cache` - separate from server-side caches.

## Verify
- [ ] Debug toolbar cache panel shows hits on repeat requests.
- [ ] Logging in as two users never shows each other's data on cached pages.
- [ ] Updating data invalidates the right keys (test asserts fresh value).

## Checked
Date: 2026-10-25. Documentation: Django documentation source (django/django main branch, 6.2 in development, commit of 2026-10-23; release notes 4.0 to 6.0) (topics/cache) and the django-redis README.
Confirmed: `django.core.cache.backends.redis.RedisCache` (added in Django 4.0), `LOCATION`, `get_or_set` with a callable, `get_many`/`set_many`, `add`, `incr_version`, `cache_page` keyed by URL, `vary_on_cookie`, `cache_control`/`never_cache`, `make_template_fragment_key`.
Corrected or removed: the `aget_or_set` example and the async description, the "including query string" key claim, and django-redis lock and `delete_pattern` claims that the README does not support.
Method: documentation only; no commands were run.

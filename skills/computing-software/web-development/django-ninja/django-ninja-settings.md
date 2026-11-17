---
id: computing-software.web-development.django-ninja.django-ninja-settings
name: django-ninja-settings
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, ninja-settings, settings, pagination, throttling, file-uploads, override-settings, pydantic]
level: practitioner
status: docs-checked
description: "Set Django Ninja's optional NINJA_* settings for pagination, throttle rates, proxies and file-upload methods, and override them in tests."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/settings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NINJA_* settings

All settings are optional; unset ones use defaults. Values are loaded once at import into a pydantic model (`ninja.conf.settings`), so they are type-checked and coerced: `"20"` works like `20`, `"not a number"` raises a validation error.

| Setting | Default |
|---|---|
| `NINJA_PAGINATION_CLASS` | `"ninja.pagination.LimitOffsetPagination"` |
| `NINJA_PAGINATION_PER_PAGE` | `100` |
| `NINJA_MAX_PER_PAGE_SIZE` | `100` |
| `NINJA_PAGINATION_MAX_LIMIT` | unbounded (`inf`) |
| `NINJA_PAGINATION_DEFAULT_ORDERING` | `("-pk",)` |
| `NINJA_DEFAULT_THROTTLE_RATES` | `{"auth": "10000/day", "user": "10000/day", "anon": "1000/day"}` |
| `NINJA_NUM_PROXIES` | `None` |
| `NINJA_FIX_REQUEST_FILES_METHODS` | `{"PUT", "PATCH", "DELETE"}` |

## Pagination

```python
# settings.py
NINJA_PAGINATION_CLASS = "ninja.pagination.LimitOffsetPagination"
NINJA_PAGINATION_PER_PAGE = 100
NINJA_MAX_PER_PAGE_SIZE = 100
NINJA_PAGINATION_MAX_LIMIT = 1000
NINJA_PAGINATION_DEFAULT_ORDERING = ("-pk",)
```

- `NINJA_PAGINATION_CLASS`: what bare `@paginate` uses.
- `NINJA_PAGINATION_PER_PAGE`: default page size/limit for the three built-in classes.
- `NINJA_MAX_PER_PAGE_SIZE`: caps client `page_size` for `PageNumberPagination` and `CursorPagination`.
- `NINJA_PAGINATION_MAX_LIMIT`: caps `limit` for `LimitOffsetPagination`; unset, a client can request an unbounded limit.
- `NINJA_PAGINATION_DEFAULT_ORDERING`: `CursorPagination` ordering when the operation passes none.

## Throttling

```python
NINJA_DEFAULT_THROTTLE_RATES = {"auth": "10000/day", "user": "10000/day", "anon": "1000/day"}
NINJA_NUM_PROXIES = 1
```
Rates apply to `AnonRateThrottle()`, `UserRateThrottle()`, `AuthRateThrottle()` built without a `rate`. `NINJA_NUM_PROXIES` is the number of trusted reverse proxies used to pick the client address from `X-Forwarded-For`; `None` uses the whole header as-is.

## File uploads

`NINJA_FIX_REQUEST_FILES_METHODS = {"PUT", "PATCH"}` sets which methods `ninja.compatibility.files.fix_request_files_middleware` parses `multipart/form-data` for to fill `request.FILES` (Django only does it for `POST`).

## Gotchas

- The pagination page-size cap is named `NINJA_MAX_PER_PAGE_SIZE` (the attribute is `PAGINATION_MAX_PER_PAGE_SIZE`); every other setting is `NINJA_` plus the attribute name.
- Tests: `@override_settings(NINJA_PAGINATION_PER_PAGE=5)` works; `ninja.conf` listens to `setting_changed` for `NINJA_*` names.
- `NINJA_DOCS_VIEW` was removed and raises at startup; pass `docs=` to `NinjaAPI`.

## Checked

2026-11-08: Read django-ninja docs/docs/guide/settings.md from GitHub. Confirmed against the whole page: the settings table with defaults, pydantic coercion and validation error, per-setting descriptions, the NINJA_MAX_PER_PAGE_SIZE naming note, override_settings and setting_changed behaviour, and the removed NINJA_DOCS_VIEW. Nothing removed.

Method: documentation only; no commands were run.

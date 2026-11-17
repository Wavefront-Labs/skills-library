---
id: computing-software.web-development.django-ninja.django-ninja-throttling
name: django-ninja-throttling
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, throttling, rate-limit, anon-rate-throttle, ninja-num-proxies, 429]
level: practitioner
status: docs-checked
description: "Rate-limit Django Ninja APIs with AnonRateThrottle, UserRateThrottle and AuthRateThrottle at API, router or operation level, with custom throttle classes."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/throttling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: limit request rates per client. Modelled on DRF throttling, but you pass initialized throttle objects, not classes.

Warning from the page: this is not a security measure (origin can be spoofed), and built-in throttles use non-atomic Django cache operations, so limits can be fuzzy under concurrency.

## Basic
```python
from ninja.throttling import AnonRateThrottle, AuthRateThrottle

api = NinjaAPI(throttle=[AnonRateThrottle("10/s"), AuthRateThrottle("100/s")])
```
If any throttle rejects, the response is 429.

Rate format `"<requests>/<period>"`; period is optional number plus optional unit (default 1, seconds). `"100/5m"`, `"100/300s"`, `"100/300"` are equivalent. Units: `s`/`sec`, `m`/`min`, `h`/`hour`, `d`/`day`.

## Levels
Most specific wins and overrides (does not add to) outer ones:
```python
router = Router(throttle=[AnonRateThrottle("1000/h")])
api.add_router("/sensitive", "myapp.api.router", throttle=AnonRateThrottle("100/m"))

@api.get("/some", throttle=[UserRateThrottle("10000/d")])
def some(request): ...
```

## Built-ins (ninja.throttling)
- `AnonRateThrottle`: only requests where `request.auth is None`; keyed by client IP.
- `UserRateThrottle`: keyed by `request.user.pk` if authenticated, else IP.
- `AuthRateThrottle`: keyed by `request.auth` (any scheme), else IP. Key is `sha256(str(request.auth))`, so give custom auth objects a unique `__str__`.

Without a rate, a throttle reads `NINJA_DEFAULT_THROTTLE_RATES` by scope (`anon`, `user`, `auth`). Page defaults: `auth` 10000/day, `user` 10000/day, `anon` 1000/day.

Behind trusted proxies set `NINJA_NUM_PROXIES = 1` (your count) in settings so the client IP is taken properly from `X-Forwarded-For`; when unset the whole header (whitespace stripped) is the identifier.

## Custom
```python
class NoReadsThrottle(AnonRateThrottle):
    def allow_request(self, request):
        if request.method == "GET":
            return True
        return super().allow_request(request)
```
For custom bucketing subclass `SimpleRateThrottle`, set `scope`, and override `get_cache_key(self, request)`; return `None` to skip throttling. Overridable attributes: `cache`, `cache_format` (`"throttle_%(scope)s_%(ident)s"`), `THROTTLE_RATES`.

## Response
429 with `{"detail": "Too many requests."}`. If `wait()` returns seconds, a rounded-up `Retry-After` header is added (longest wait among rejecting throttles). Customize by registering a handler for `ninja.errors.Throttled`.

## Checked
Confirmed 2026-11-08 against the Django Ninja throttling guide (docs/docs/guide/throttling.md, read in full): warning text, rate format and units, override order, the three built-in throttles and their keys, default rates, `NINJA_NUM_PROXIES`, custom throttle hooks and class attributes, and the 429 response with `Retry-After`. Nothing removed.
Method: docs-only read of cited pages, 2026-11-08

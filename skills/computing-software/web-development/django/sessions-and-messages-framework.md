---
id: computing-software.web-development.django.sessions-and-messages-framework
name: sessions-and-messages-framework
category: computing-software
field: web-development
product: django
tags: [django-sessions, messages-framework, session-backends, flash-messages, django]
level: practitioner
status: verified
description: "Using Django sessions and the messages framework: session backends and settings, storing data safely, session security, flash messages in templates and accessible message display."
sources:
  - https://docs.djangoproject.com/en/stable/topics/http/sessions/
  - https://docs.djangoproject.com/en/stable/ref/contrib/messages/
  - https://docs.djangoproject.com/en/stable/ref/settings/#sessions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sessions and the messages framework

## 1. Session backends
| Backend | `SESSION_ENGINE` | Use |
|---|---|---|
| Database (default) | `django.contrib.sessions.backends.db` | simple; run `clearsessions` periodically |
| Cache | `...backends.cache` | fast, but sessions lost on cache eviction/restart |
| Cached DB | `...backends.cached_db` | cache reads with DB durability - good default at scale |
| Signed cookies | `...backends.signed_cookies` | no server storage; data visible to client (signed, not encrypted), size-limited, can't revoke |

## 2. Settings
```python
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True        # default
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False    # True gives sliding expiry at the cost of a write per request
```

## 3. Using sessions
```python
request.session["cart"] = {"items": [...]}       # must be JSON-serialisable (default `SESSION_SERIALIZER` is the JSON serializer; saving a `datetime` raised TypeError)
request.session["cart"]["items"].append(x)       # nested mutation is NOT detected...
request.session.modified = True                  # ...so mark it (run on 6.1.2: without it the append was lost, with it the session held [1, 3])
request.session.set_expiry(300)                  # per-session override
request.session.cycle_key()                      # new key, keep data (Django calls this on login)
request.session.flush()                          # logout: delete data and cookie
```
- Don't store large objects or model instances; store ids.
- Session fixation is handled by `login()` rotating the key; call `cycle_key()` yourself after privilege changes outside login.

## 4. Messages framework
```python
from django.contrib import messages
messages.success(request, "Profile updated.")
messages.error(request, "Payment failed. Your card was not charged.")
return redirect("profile")                       # post/redirect/get, message shown on next page
```
```django
{% if messages %}
<div class="messages" role="status" aria-live="polite">
  {% for m in messages %}<p class="msg msg-{{ m.tags }}">{{ m }}</p>{% endfor %}
</div>{% endif %}
```
- Storage: `FallbackStorage` (cookie, then session) is the default (checked in `settings.MESSAGE_STORAGE`; the response set a `messages` cookie). Messages are consumed when iterated.
- Use `role="alert"` for errors that need immediate attention; don't auto-dismiss important messages quickly (WCAG 2.2.1).
- `MESSAGE_TAGS = {messages.ERROR: "danger"}` to map to CSS framework classes.
- With HTMX/AJAX, render messages in responses (e.g. out-of-band swaps) since there's no full page load.

## Verify
- [ ] Session cookies Secure/HttpOnly/SameSite; expired sessions cleaned up; flash messages appear once after redirects and are announced by screen readers.

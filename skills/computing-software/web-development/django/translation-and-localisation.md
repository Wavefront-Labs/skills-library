---
id: computing-software.web-development.django.translation-and-localisation
name: translation-and-localisation
category: computing-software
field: web-development
product: django
tags: [django, django-i18n, gettext, makemessages, localization, i18n-patterns, timezones, python, web-development]
level: practitioner
status: docs-checked
description: "Internationalising Django: gettext and lazy translation, makemessages/compilemessages, plural forms, LocaleMiddleware and i18n_patterns, formats and timezones."
sources:
  - https://docs.djangoproject.com/en/stable/topics/i18n/translation/
  - https://docs.djangoproject.com/en/stable/topics/i18n/formatting/
  - https://docs.djangoproject.com/en/stable/topics/i18n/timezones/
  - https://docs.djangoproject.com/en/stable/ref/django-admin/#makemessages
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Translation and localisation

**Goal:** every user-facing string translatable, dates/numbers formatted per locale, and language chosen predictably.

## 1. Settings
```python
USE_I18N = True
USE_TZ = True                     # store UTC, display local
LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English"), ("de", "Deutsch"), ("fr", "Français")]
LOCALE_PATHS = [BASE_DIR / "locale"]
MIDDLEWARE = [..., "django.contrib.sessions.middleware.SessionMiddleware",
              "django.middleware.locale.LocaleMiddleware",           # after sessions, before common
              "django.middleware.common.CommonMiddleware", ...]
```

## 2. Marking strings
```python
from django.utils.translation import gettext as _, gettext_lazy, ngettext, pgettext
class Order(models.Model):
    status = models.CharField(_("status") ...)            # wrong at import time
    status = models.CharField(gettext_lazy("status"), ...)  # right: lazy for module-level strings
msg = ngettext("%(n)d item", "%(n)d items", n) % {"n": n}
label = pgettext("month name", "May")                      # context disambiguates
```
Use named placeholders so translators can reorder. Never concatenate translated fragments.

Templates:
```django
{% load i18n %}
<h1>{% translate "Your orders" %}</h1>
{% blocktranslate count n=orders|length %}{{ n }} order{% plural %}{{ n }} orders{% endblocktranslate %}
```
JavaScript: `JavaScriptCatalog` view + `gettext()` in JS.

## 3. Catalog workflow
```bash
python manage.py makemessages -l de -l fr --ignore=venv/*
# translate locale/de/LC_MESSAGES/django.po (Poedit, Weblate, Crowdin)
python manage.py compilemessages
```
Fuzzy entries (`#, fuzzy`) are ignored at runtime until reviewed. Compile `.mo` in the build; don't commit stale `.mo` files.

## 4. Choosing the language
`LocaleMiddleware` checks: URL prefix (`i18n_patterns`), `django_language` cookie, `Accept-Language`, then `LANGUAGE_CODE`.
```python
urlpatterns += i18n_patterns(path("shop/", include("shop.urls")), prefix_default_language=False)
```
URL prefixes give crawlable per-language URLs; add `hreflang` links. `set_language` view switches language via POST.

## 5. Formats and time zones
`{{ value|date:"SHORT_DATE_FORMAT" }}`, `{% localize on %}`, number formatting with `USE_THOUSAND_SEPARATOR`. With `USE_TZ`, activate per-user zones in middleware: `timezone.activate(zoneinfo.ZoneInfo(user.tz))`. Never use naive `datetime.now()` - use `timezone.now()`.

## Verify
- [ ] `makemessages` produces no new untranslated entries for shipped languages (CI check on `.po` coverage).
- [ ] Pseudo-locale or German run reveals no hard-coded English or truncated layouts.
- [ ] Dates render in the user's timezone; DB values are UTC.

## Checked
Date: 2026-10-25. Documentation: Django documentation source (django/django main branch, 6.2 in development, commit of 2026-10-23; release notes 4.0 to 6.0) (topics/i18n/translation, formatting, timezones, ref/django-admin, ref/settings).
Confirmed: `LocaleMiddleware` placement after `SessionMiddleware` and before `CommonMiddleware`, language order (URL prefix, `django_language` cookie via `LANGUAGE_COOKIE_NAME`, `Accept-Language`, `LANGUAGE_CODE`), `i18n_patterns(prefix_default_language=False)`, `set_language` view via POST, `JavaScriptCatalog`, fuzzy entries skipped by `compilemessages`, `--ignore` pattern option, `pgettext`, `{% localize on %}`, `USE_THOUSAND_SEPARATOR`, `timezone.activate(zoneinfo.ZoneInfo(...))`.
Nothing needed correcting.
Method: documentation only; no commands were run.

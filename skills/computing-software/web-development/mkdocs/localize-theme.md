---
id: computing-software.web-development.mkdocs.localize-theme
name: localize-theme
category: computing-software
field: web-development
product: mkdocs
tags: [locale, i18n, theme-localization, iso-639-1]
level: practitioner
status: docs-checked
description: "Show the theme UI in another language with theme.locale after installing mkdocs[i18n]; it does not translate page content."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/localizing-your-theme.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/choosing-your-theme.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Localization translates only the theme's own text ("next", "previous"), not your documentation. For multilingual content, combine it with a third-party internationalization plugin.

```bash
pip install 'mkdocs[i18n]'
```

```yaml
theme:
  name: mkdocs
  locale: fr
```

Locale format: usually the ISO-639-1 two-letter code, optionally with a territory after an underscore (`en`, `en_AU`, `en_GB`, `en_US`).

Gotchas:
- Needs a theme that supports it; supported locales are listed in each theme's docs (`mkdocs` and `readthedocs` list `en` plus the directories under their `locales` folders).
- An unsupported locale falls back to the theme's default locale.
- `theme.locale` also sets the search plugin default `lang`.

Missing translation? See `theme-translation-workflow`.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Localizing your theme" (install `mkdocs[i18n]`, locale format, fallback, usage), "Choosing your theme" (`locale` per theme) and "Configuration" (search `lang` default is `theme.locale` if set). Removed the Verify line, which the pages do not state.
Method: documentation only; no commands were run.

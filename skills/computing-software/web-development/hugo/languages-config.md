---
id: computing-software.web-development.hugo.languages-config
name: languages-config
category: computing-software
field: web-development
product: hugo
tags: [languages, multilingual-config, default-content-language, multihost, language-weight]
level: practitioner
status: docs-checked
description: "Configure Hugo languages: defaultContentLanguage, subdirectory publishing, language keys, label, locale, direction, weight order, localized settings and multihost baseURL."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/languages.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Base settings:

```toml
defaultContentLanguage = 'en'
defaultContentLanguageInSubdir = false
disableLanguages = []
```

`defaultContentLanguage` uses RFC 5646 syntax and must match a defined language key. `defaultContentLanguageInSubdir` (default `false`) publishes the default language in a subdirectory.

Per-language settings under `languages`: `label` (for a language switcher), `locale`, `direction` (`ltr` default, or `rtl`), `title`, `weight`, `disabled`. `languageCode`, `languageDirection` and `languageName` were deprecated in 0.158.0; use `locale`, `direction` and `label`.

Languages sort by weight ascending, then lexicographically; this affects build order and complement selection. Some keys can be localized; an undefined key falls back to the root value.

```toml
[languages.en]
label = 'English'
locale = 'en-US'
timeZone = 'America/New_York'
title = 'Project Documentation'
weight = 1
[languages.en.pagination]
path = 'page'
```

Language keys follow RFC 5646; private use subtags cannot exceed 8 alphanumeric characters.

**Multihost:** give each language a unique `baseURL`. If one language defines it, all must. Hugo then publishes `public/en` and `public/fr`.

```toml
[languages.fr]
baseURL = 'https://fr.example.org'
weight = 1
```

## Checked

2026-11-04. Confirmed against the Hugo docs page Configure languages: the base settings and defaults, RFC 5646 keys and the 8-character private use limit, per-language settings, the 0.158.0 deprecations, sort order, localized settings with root fallback and the multihost `baseURL` rule and `public` layout. Nothing removed.

Method: documentation only; no commands were run.

---
id: computing-software.web-development.hugo.multilingual-content
name: multilingual-content
category: computing-software
field: web-development
product: hugo
tags: [multilingual, translations, translationkey, i18n, missing-translations]
level: practitioner
status: docs-checked
description: "Build multilingual Hugo content: translate by file name or directory, link translations with translationKey, localize slugs and menus, and find missing translations."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/multilingual.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**By file name:** a language code suffix assigns the language, and matching paths and base names link translations. Codes are lowercase (`about.en-us.md`, not `about.en-US.md`). Files without a code go to the default language.

**By directory:** each language's `contentDir` sets its content directory; directories cannot overlap.

```toml
[languages.en]
contentDir = 'content/english'
label = "English"
weight = 10
```

**Bypass default linking:** pages sharing a `translationKey` value are translations, regardless of name or location.

```yaml
translationKey: "about"
```

**Localize URLs** with `slug` or `url` (for example `slug: "a-propos"` in `content/about.fr.md`).

**Strings and formats:** `lang.Translate` for strings; `time.Format` for dates; `lang.FormatCurrency`, `lang.FormatNumber`, `lang.FormatPercent`.

```go-html-template
{{ 512.5032 | lang.FormatCurrency 2 "USD" }}
```

**Menus:** entries look up translations by `identifier`, falling back to `name`.

```go-html-template
{{ or (T .Identifier) .Name | safeHTML }}
```

**Missing translations** fall back to the default language value, or an empty string. `enableMissingTranslationPlaceholders` flags them as `[i18n] identifier` (not for production). Find them:

```sh
hugo build --printI18nWarnings
```

Theme URLs must come from `.Permalink` or `.RelPermalink`, `urls.RelLangURL` or `urls.AbsLangURL`, or use the `{{ .LanguagePrefix }}` prefix.

## Checked

2026-11-04: lowercase language code rule, default-language fallback, contentDir and non-overlap rule, translationKey, slug/url localization, formatting functions, menu identifier lookup, missing-translation behaviour and --printI18nWarnings, and theme URL rules confirmed against the Hugo docs Multilingual mode page. Nothing removed.

Method: documentation only; no commands were run.

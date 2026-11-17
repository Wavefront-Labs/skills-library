---
id: computing-software.web-development.hono.hono-language-detector
name: hono-language-detector
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, i18n, language, locale]
level: practitioner
status: docs-checked
description: "Detect user locale in Hono with languageDetector: query, cookie, header and path sources, fallback, progressive matching and cookie caching."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/language.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Language detector

Import: `import { languageDetector } from 'hono/language'`. It sets `c.get('language')`.

```ts
app.use(languageDetector({
  supportedLanguages: ['en', 'ar', 'ja'], // must include fallback
  fallbackLanguage: 'en', // required
}))
app.get('/', (c) => c.text(`Hello! Your language is ${c.get('language')}`))
```

Tests: `curl http://localhost:8787/?lang=ar`, `curl -H 'Cookie: language=ja' ...`, `curl -H 'Accept-Language: ar,en;q=0.9' ...`.

## Defaults
`order: ['querystring','cookie','header']`, `lookupQueryString: 'lang'`, `lookupCookie: 'language'`, `lookupFromHeaderKey: 'accept-language'`, `lookupFromPathIndex: 0`, `caches: ['cookie']`, `ignoreCase: true`, `debug: false`, cookie `{ sameSite: 'Strict', secure: true, maxAge: 365*24*60*60, httpOnly: true }`.

## Recipes
Path first (`/en/about`): `order: ['path','cookie','querystring','header']` with `lookupFromPathIndex: 0`.

Progressive matching: with `supportedLanguages: ['en','ja','zh-Hant']`, `ja-JP` matches `ja` and `zh-Hant-CN` matches `zh-Hant` (exact match preferred).

Normalise: `convertDetectedLanguage: (lang) => lang.split('-')[0]`.

Cookie control: `cookieOptions: { path: '/', sameSite: 'Lax', secure: true, maxAge: 86400 * 365, httpOnly: true, domain: '.example.com' }`; disable caching with `caches: false`. Log with `debug: true`.

## Gotchas
- `fallbackLanguage` must be in `supportedLanguages`; otherwise setup throws. `lookupFromPathIndex` must be >= 0. Invalid config throws at initialisation.
- Failed detections silently use the fallback.
- The default cookie is `secure: true`, so it will not be sent over plain HTTP.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/language.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.

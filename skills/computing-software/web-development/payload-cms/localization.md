---
id: computing-software.web-development.payload-cms.localization
name: localization
category: computing-software
field: web-development
product: payload-cms
tags: [localization, locales, fallback-locale, localized-fields]
level: practitioner
status: docs-checked
description: "Enable content localization with locales and defaultLocale, mark fields localized, and request a locale or fallback locale in the APIs."
sources:
  - https://payloadcms.com/docs/configuration/localization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Localization

Goal: store field values per language.

```ts
export default buildConfig({
  localization: {
    locales: ['en', 'es', 'de'],   // required
    defaultLocale: 'en',           // required
    fallback: true,                // defaults to true
  },
})
```

Locales can be objects: `code` (required, unique), `label` (string or object keyed by i18n language), `rtl`, and `fallbackLocale` (single code or array).

Other options: `fallback` (boolean, return the fallback value when a locale value is missing) and `filterAvailableLocales` (function receiving `locales` and `req`, returns the locales shown in the admin selector).

Mark individual fields with `localized: true`; this needs localization enabled in the base config.

Request a locale with the `locale` and `fallbackLocale` options (Local API) or `?locale=es&fallback-locale=en` (REST). The REST parameter names are `locale` and `fallback-locale`.

Verify: `GET /api/pages?locale=es` returns the Spanish values.

## Checked

2026-11-04. Read configuration/localization. Confirmed: locales and defaultLocale as required, locale object keys (code, label, rtl, fallbackLocale), fallback (default true), filterAvailableLocales with locales and req, localized: true on fields, and the REST locale and fallback-locale query parameters.
Method: documentation only; no commands were run.

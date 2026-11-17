---
id: computing-software.web-development.eleventy.i18n-plugin
name: i18n-plugin
category: computing-software
field: web-development
product: eleventy
tags: [i18n-plugin, locale-url, locale-links, page-lang, errormode]
level: practitioner
status: docs-checked
description: "Use Eleventy's bundled i18n plugin: defaultLanguage, errorMode, the locale_url and locale_links filters, page.lang and localized collection navigation."
sources:
  - https://www.11ty.dev/docs/plugins/i18n/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Bundled since v2.0.0. It manages links between localized content; it does not translate strings (pick a library for that).

```js
import { I18nPlugin } from "@11ty/eleventy";

export default function (eleventyConfig) {
  eleventyConfig.addPlugin(I18nPlugin, {
    defaultLanguage: "en",         // required, any BCP 47 tag
    filters: { url: "locale_url", links: "locale_links" }, // rename filters
    errorMode: "strict",           // or "allow-fallback" or "never"
  });
}
```

- **`page.lang`**: the page's language tag; defaults to `defaultLanguage`.
- **`locale_url`**: rewrites any URL for the current page's locale. `"/blog/"`, `"/en/blog/"` and `"/es/blog/"` all give `/es/blog/` on a Spanish page. It checks the target file exists; a missing localized file throws under `strict`. A second argument overrides the locale.
- **`locale_links`**: array of alternatives for a URL (default current page), excluding the original, each `{ url, lang, label }`, e.g. `{ "url": "/es/blog/", "lang": "es", "label": "Espanol" }`. Use it for "also available in" links or `<link rel="alternate">` (hrefs must be fully qualified).
- With i18n added, `getCollectionItem`, `getPreviousCollectionItem` and `getNextCollectionItem` prefer items in the current page language, falling back to the default language:

```njk
{%- set nextPost = collections.post | getNextCollectionItem %}
{%- if nextPost %}<a href="{{ nextPost.url | locale_url }}">Next post</a>{% endif %}
```

Read the i18n strategy skill first for folder and URL decisions.

## Checked

2026-11-04. Confirmed against the Eleventy Internationalization plugin page: bundled from v2.0.0, links only and no string localization, defaultLanguage (required, BCP 47), filters renaming, the three errorMode values, page.lang defaulting to defaultLanguage, locale_url behavior (language code swap, existence check, second-argument override), locale_links output shape and exclusion of the original page, fully qualified alternate hrefs, and the get*CollectionItem preference with default-language fallback. Corrected the version gate from 2.0.0-canary.13.

Method: documentation only; no commands were run.

---
id: computing-software.web-development.eleventy.i18n-strategy
name: i18n-strategy
category: computing-software
field: web-development
product: eleventy
tags: [i18n, localization, locale-folders, content-negotiation, netlify-redirects]
level: practitioner
status: docs-checked
description: "Plan a multi-language Eleventy site: locale folders and directory data, distinct URLs versus content negotiation, and Netlify redirect patterns."
sources:
  - https://www.11ty.dev/docs/i18n/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two up-front decisions: file organisation and URL style.

**Files.** Most projects use a folder per locale (`en/about.html`, `es/about.html`), which suits the data cascade and default permalinks. A directory data file such as `en/en.json` with `{"lang": "en"}` sets `lang` for everything inside. File-name codes (`about.en.html`) are unwieldy and not recommended, though possible with permalink wrangling.

**URL style.**

- Distinct URLs (`/en/about/`, `/es/about/`): every page addressable and cacheable, easy static hosting. Cost: internal links need normalizing (use the plugin's `locale_url`), and a redirect on language mismatch is only suggested (use `locale_links` to show alternatives).
- Content negotiation (`/about/`): server picks content from `Accept-Language`. No redirects needed, but needs server config and gives users less control.

Mixing is fine. Netlify `_redirects` patterns (en default, es extra):

```
# Content negotiation on / only, distinct URLs elsewhere
/   /es/        200   Language=es
/   /en/        200
/*  /es/:splat  302   Language=es
/*  /en/:splat  302
```

Read Netlify's shadowing rules: existing `/es/*` and `/en/*` files are served without redirects. Libraries such as `i18next` or `intl-messageformat` handle string localization.

## Checked

2026-11-04. Confirmed against the Eleventy Internationalization page: the two up-front decisions, folder-per-locale with directory data files setting lang, file-name codes being unwieldy and not recommended, the pros and cons of distinct URLs and content negotiation, locale_url and locale_links references, the mixed approach and the Netlify redirect patterns with the shadowing note. Nothing removed.

Method: documentation only; no commands were run.

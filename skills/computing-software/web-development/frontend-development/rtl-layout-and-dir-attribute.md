---
id: computing-software.web-development.frontend-development.rtl-layout-and-dir-attribute
name: rtl-layout-and-dir-attribute
category: computing-software
field: web-development
product: frontend-development
tags: [intl-api, rtl-layout, dir-attribute, bidi, logical-properties, i18n]
level: practitioner
status: docs-checked
description: "Supporting right-to-left languages: lang and dir on html, dir=auto for user text, bdi, logical CSS properties, mirroring icons, and testing Arabic and Hebrew layouts."
sources:
  - https://www.w3.org/International/questions/qa-html-dir
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/dir
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/bdi
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Logical_properties_and_values
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RTL layouts, lang and dir

## 1. Document level
```html
<html lang="ar" dir="rtl">
```
Set server-side per locale (Arabic, Hebrew, Persian, Urdu, Pashto, Yiddish and Dhivehi are among the right-to-left languages). `new Intl.Locale("ar").getTextInfo?.().direction` gives it where supported (Chrome 130, Safari 17, Firefox 153). Never use CSS to apply the base direction: the directional information must be available even when the CSS is not.

## 2. Mixed and user content
- User-generated text of unknown direction: `<p dir="auto">`, and `dir="auto"` on inputs/textareas.
- Inline user content in a sentence: `<bdi>username</bdi>` isolates it so "Ahmed: 5 reviews" does not scramble punctuation.

## 3. CSS: logical properties
| Physical | Logical |
|---|---|
| `margin-left` | `margin-inline-start` |
| `padding-right` | `padding-inline-end` |
| `left: 0` | `inset-inline-start: 0` |
| `text-align: left` | `text-align: start` |
| `border-top-left-radius` | `border-start-start-radius` |
Flexbox and grid already follow `dir`. Selector fallback for remaining cases: `:dir(rtl)` (Chrome 120, Firefox 49, Safari 16.4) or `[dir="rtl"] &`. Tailwind: `ms-4`/`me-4`, `rtl:` variant.

## 4. Mirroring
- Mirror directional icons (back/forward arrows, progress, sliders): `:dir(rtl) .icon-arrow { transform: scaleX(-1) }`.

## Verify
- Toggle `dir="rtl"` on `<html>` in DevTools for a quick smoke test; then pseudo-localize with real Arabic/Hebrew strings.
- Check focus order and keyboard arrow behaviour in sliders/carousels are mirrored.

## Checked
2026-10-26. W3C Internationalization article on html dir, MDN dir, bdi and logical properties pages, Tailwind docs and browser-compat-data (main, 2026-10-26): confirmed dir=auto uses the first strongly typed character and skips bdi, never use CSS for the base direction, the RTL language list used, the logical property names in the table, the :dir() and Intl.Locale getTextInfo support versions, and Tailwind ms-/me- and rtl: variants. Removed the unconfirmed number and form-input direction advice, the mirroring do-not-mirror list, the typography paragraph and the dead Material link.
Method: documentation only; no commands were run.

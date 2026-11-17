---
id: computing-software.web-development.web-accessibility.language-of-page-and-parts
name: language-of-page-and-parts
category: computing-software
field: web-development
product: web-accessibility
tags: [readable, predictable, lang-attribute, language-of-page, language-of-parts, wcag-3-1-1, wcag-3-1-2, screen-reader-pronunciation, hreflang]
level: practitioner
status: verified
description: "Meeting WCAG 3.1.1 and 3.1.2: correct html lang, lang on passages in other languages, language switchers, and how lang drives speech, hyphenation and fonts."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html
  - https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts.html
  - https://www.w3.org/International/questions/qa-choosing-language-tags
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Language of page and parts

**Goal:** screen readers pronounce text with the right voice and rules, and browsers apply correct hyphenation, quotes and fonts.

## 1. Page language (3.1.1, A)
```html
<html lang="en-GB">
```
- BCP 47 tags: `en`, `en-GB`, `pt-BR`, `zh-Hans`, `sr-Latn` (all accepted by `Intl.getCanonicalLocales`; axe `html-has-lang` flags a missing attribute and `valid-lang` a bad part value such as `lang="xx1"`, run). Keep it simple - region subtags only when it matters.
- Set it server-side per locale; SPAs that switch language must update `document.documentElement.lang` (Next.js: `<html lang={locale}>` in the root layout per locale segment; Nuxt i18n/`useHead({ htmlAttrs: { lang } })`).
- Missing/wrong `lang` makes a French screen reader read English pages with French pronunciation (and vice versa).

## 2. Parts in other languages (3.1.2, AA)
```html
<p>The motto was <span lang="la">Festina lente</span>.</p>
<a href="/de/" lang="de" hreflang="de">Deutsch</a>     <!-- language switcher: each option in its own language -->
```
Exceptions: proper names, technical terms, words that have become part of the surrounding language ("café" in English).

## 3. Direction
For RTL languages add `dir="rtl"` (on `<html>` or the element); `dir="auto"` for user-generated content of unknown direction. Use logical CSS properties so layouts mirror.

## 4. Side effects of lang
- `hyphens: auto` needs `lang` to work.
- `:lang()` selector for language-specific styles (quotes, fonts for CJK).
- Browser translation and spellcheck use it.
- Fonts: CJK text with the wrong `lang` may render with the wrong glyph variants (Han unification).

## Verify
- [ ] axe `html-has-lang`, `html-lang-valid`, `valid-lang` pass.
- [ ] Screen reader switches voice for foreign-language passages (NVDA/JAWS with automatic language switching).
- [ ] Locale switch updates `<html lang>` in the SPA.

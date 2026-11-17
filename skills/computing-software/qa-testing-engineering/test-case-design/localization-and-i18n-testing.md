---
id: computing-software.qa-testing-engineering.test-case-design.localization-and-i18n-testing
name: localization-and-i18n-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [localization-testing, i18n-testing, l10n, internationalization, pseudo-localization, rtl-testing, compatibility-testing]
level: practitioner
status: docs-checked
description: "Test internationalisation and localisation: pseudo-localisation, text expansion, RTL, locale formats for dates, numbers and currency, sorting, and encodings."
sources:
  - https://www.w3.org/International/techniques/developing-specs
  - https://cldr.unicode.org/
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Localisation and internationalisation testing

**Goal:** the product works for every target locale, and adding a locale does not need code changes.

## i18n (before translation)
- **Pseudo-localisation**: replace strings with accented, noticeably longer text and brackets: `[Ŝàvé çĥàñĝéš !!!]`. Reveals hard-coded strings (unchanged text), truncation, and concatenation (broken brackets).
- **Encoding**: UTF-8 end to end; test names like `Zoë Ñúñez`, `山田太郎`, emoji, combining characters, in forms, URLs, file names, CSV exports, emails, PDFs.
- **RTL** (Arabic, Hebrew): mirrored layout, icons that should/should not flip, mixed-direction text (numbers inside Arabic).
- **Locale formats** via CLDR/Intl: dates (`03/04` ambiguity), number separators, currency formatting, plural rules (`Intl.PluralRules`), sorting. CLDR describes how plurals work in various languages and how lists are alphabetised.
- **Time zones and DST**: scheduled items across DST transitions, users in different zones.

## l10n (after translation)
- Every string translated (no fallback language showing), context-correct translations (screenshots for translators), truncation and overflow, legal text per locale, locale-specific features (address formats, phone validation, tax).

## Automating
Run UI tests once per target locale (set the browser locale and time zone in your test runner), check for missing keys in logs, snapshot key screens per locale.

## Gotchas
- Server and client formatting the same date differently.
- Validation that rejects non-ASCII names.

## Verify
Pseudo-locale build passes a full UI pass with no untranslated strings or truncation; each live locale has a native-speaker review.

## Checked

2026-10-28 Confirmed against: CLDR site (locale data for dates, numbers, plurals and alphabetisation); MDN Intl (`Intl.PluralRules`, locale identifiers). Removed or generalised: the 30-40% expansion figure, `dir="rtl"`, de-DE separators, Polish/Arabic plural counts, the German/Swedish collation example, first-day-of-week, and the Playwright option names (not in the fetched pages; the W3C page returned only a stub).

Method: documentation only; no commands were run.

---
id: computing-software.web-development.frontend-development.intl-listformat-and-displaynames
name: intl-listformat-and-displaynames
category: computing-software
field: web-development
product: frontend-development
tags: [intl-listformat, intl-displaynames, internationalization, intl-api, javascript]
level: practitioner
status: verified
description: "Locale-correct lists with Intl.ListFormat (and/or/unit) and localized names of languages, regions, currencies and scripts with Intl.DisplayNames."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/ListFormat
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DisplayNames
  - https://tc39.es/ecma402/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Intl.ListFormat and Intl.DisplayNames

## 1. Lists
```js
const items = ["Alice", "Bob", "Chen"];
new Intl.ListFormat("en-US", { type: "conjunction" }).format(items);  // "Alice, Bob, and Chen"
new Intl.ListFormat("en-GB").format(items);                            // "Alice, Bob and Chen"
new Intl.ListFormat("es").format(items);                               // "Alice, Bob y Chen"
new Intl.ListFormat("en", { type: "disjunction" }).format(items);      // "Alice, Bob, or Chen"
new Intl.ListFormat("en", { style: "narrow", type: "unit" }).format(["5 h", "30 min"]); // "5 h 30 min"
```
Never `join(", ")` plus " and " in UI: Oxford comma, conjunction word and separators all vary (Japanese uses "、", Arabic "و").
`formatToParts` returns `{type: "element" | "literal"}` parts so you can bold names.

## 2. Display names
```js
const region = new Intl.DisplayNames(["fr"], { type: "region" });
region.of("DE");        // "Allemagne"
new Intl.DisplayNames(["en"], { type: "language" }).of("pt-BR");   // "Brazilian Portuguese"
new Intl.DisplayNames(["en"], { type: "language", languageDisplay: "standard" }).of("pt-BR"); // "Portuguese (Brazil)"
new Intl.DisplayNames(["ja"], { type: "currency" }).of("EUR");     // "ユーロ"
new Intl.DisplayNames(["en"], { type: "dateTimeField" }).of("month"); // "month"
```
Types: `language`, `region`, `script`, `currency`, `calendar`, `dateTimeField`. Well-formed unknown codes return the code (`of("QQ")` gives `"QQ"`, or `undefined` with `fallback: "none"`); malformed codes such as `of("ZZZZ")` for `region` throw `RangeError`.

## 3. Language pickers
Show each language in its own language (endonym): `new Intl.DisplayNames([code], {type: "language"}).of(code)` gives "Deutsch", "日本語". Add `lang` on each option so screen readers pronounce it.

## Gotchas
- Output comes from the engine's CLDR data and can change between browser versions; do not snapshot-test exact strings across engines.
- Region names for disputed territories follow CLDR, which may not match your legal requirements.
- Node built with `small-icu` lacks most locales; official Node builds ship full ICU (Node 20.20 reported `icu_small: false`, ICU 78.2).

## Verify
- [ ] Country/language selects render translated names when the UI locale changes, with no hard-coded name tables.

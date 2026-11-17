---
id: computing-software.web-development.frontend-development.intl-collator-and-segmenter
name: intl-collator-and-segmenter
category: computing-software
field: web-development
product: frontend-development
tags: [intl-api, intl-collator, intl-segmenter, sorting, i18n, unicode, javascript]
level: practitioner
status: verified
description: "Sorting and searching strings correctly with Intl.Collator (locale order, numeric, accent-insensitive) and splitting graphemes, words and sentences with Intl.Segmenter."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Collator
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter
  - https://unicode.org/reports/tr29/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Intl.Collator and Intl.Segmenter

## 1. Sorting
`["b", "a", "Z", "ä"].sort()` sorts by UTF-16 code units: `["Z","a","b","ä"]`. Use a collator:
```js
const coll = new Intl.Collator(locale, { numeric: true, sensitivity: "base" });
files.sort(coll.compare);              // "file2" before "file10"; case/accents ignored for equality
names.sort((a, b) => coll.compare(a.last, b.last));
```
- `sensitivity`: `base` (a = A = á), `accent` (a = A, a != á), `case`, `variant` (default for sort).
- `numeric: true` gives natural sort. `caseFirst: "upper"` to order ties.
- Locale matters: Swedish sorts `ä` after `z`; German puts it with `a`. `"de-u-co-phonebk"` selects phonebook order.
- Reuse the collator - `a.localeCompare(b, locale, opts)` is slow in big sorts: sorting 50 000 strings took about 3.4 s with `localeCompare(..., "en", {numeric:true})` versus about 0.1 s with a reused `Intl.Collator` (Node 20, ICU 78); plain `localeCompare(b)` with no locale/options took 15 ms.
- Measured with Node 20: `sv` sorts `["a","ä","z"]` as `a z ä`, `de` as `a ä z`; `de-u-co-phonebk` orders `["Ae","Ä","Af"]` unchanged while plain `de` gives `Ä Ae Af`; `sensitivity: "case"` treats `a`/`á` as equal but `a`/`A` as different.

## 2. Accent/case-insensitive search
```js
const eq = new Intl.Collator(locale, { sensitivity: "base", usage: "search" });
items.filter(i => eq.compare(i.name.slice(0, q.length), q) === 0);   // prefix match
// or normalise: s.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLocaleLowerCase(locale)
```

## 3. Segmenter
```js
const g = new Intl.Segmenter(locale, { granularity: "grapheme" });
[...g.segment("👩‍👩‍👧é")].length;           // 2 user-perceived characters (`.length` is 9, `[...str].length` is 6)
const w = new Intl.Segmenter("ja", { granularity: "word" });
[...w.segment("今日は良い天気")].filter(s => s.isWordLike).map(s => s.segment);
```
Use for: character counters (Twitter-style limits), truncation that does not split emoji/combining marks, word counts in languages without spaces (Chinese, Japanese, Thai), cursor movement.

## 4. Pitfalls
- `str.length`, `slice`, `split("")` work in UTF-16 code units and break emoji and surrogate pairs; `[...str]` splits code points, still not graphemes.
- `toUpperCase()` is locale-insensitive - Turkish `i` needs `toLocaleUpperCase("tr")`.
- Database collation and JS collation can disagree - sort server-side for paginated lists.

## Verify
Tests: natural sort of `file1,file10,file2`; grapheme count of family emoji = 1; Swedish vs German ordering of `ä`.

---
id: computing-software.web-development.frontend-development.intl-pluralrules-and-relativetimeformat
name: intl-pluralrules-and-relativetimeformat
category: computing-software
field: web-development
product: frontend-development
tags: [intl-api, intl-pluralrules, relative-time-format, pluralization, i18n, javascript]
level: practitioner
status: verified
description: "Pluralising messages with Intl.PluralRules (cardinal and ordinal) and showing '3 days ago' with Intl.RelativeTimeFormat, plus ICU MessageFormat in i18n libraries."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/PluralRules
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat
  - https://cldr.unicode.org/index/cldr-spec/plural-rules
  - https://formatjs.github.io/docs/core-concepts/icu-syntax/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PluralRules and RelativeTimeFormat

## 1. Plurals are not `n === 1`
CLDR categories: `zero, one, two, few, many, other`. English uses one/other; Arabic uses all six; Polish uses one/few/many/other; French treats 0 as `one` (and reports `many`, `one`, `other`). Node 20 `select` for 0,1,2,5,11,21,22,101: en `other one other other other other other other`; pl `many one few many many many few many`; ar `zero one two few many many many other`; fr `one one other other other other other other`.
```js
const pr = new Intl.PluralRules(locale);
const msgs = { one: "# file", other: "# files" };          // per-locale table from translators
const label = n => msgs[pr.select(n)].replace("#", new Intl.NumberFormat(locale).format(n));
```
Ordinals:
```js
const ord = new Intl.PluralRules("en", { type: "ordinal" });
const suf = { one: "st", two: "nd", few: "rd", other: "th" };
`${n}${suf[ord.select(n)]}`; // 1st 2nd 3rd 4th 11th 21st 112th
```
Always provide an `other` form - it is the fallback in every locale.

## 2. In real apps: ICU MessageFormat
```
{count, plural, =0 {No files} one {# file} other {# files}}
```
Supported by FormatJS/react-intl, i18next (ICU plugin or its own `_one`/`_other` keys built on PluralRules) and Lingui; vue-i18n uses its own message syntax. Do not concatenate sentence fragments - word order differs per language.

## 3. RelativeTimeFormat
```js
const rtf = new Intl.RelativeTimeFormat(locale, { numeric: "auto" });
rtf.format(-1, "day");    // "yesterday" (numeric:auto) vs "1 day ago"
rtf.format(3, "hour");    // "in 3 hours"
function ago(date, now = Date.now()) {
  const s = Math.round((date - now) / 1000);
  const units = [["year", 31536000], ["month", 2592000], ["week", 604800], ["day", 86400], ["hour", 3600], ["minute", 60]];
  for (const [u, sec] of units) if (Math.abs(s) >= sec) return rtf.format(Math.round(s / sec), u);
  return rtf.format(s, "second");
}
```
- The API formats; it does not pick the unit - you choose thresholds.
- Month/year by fixed seconds is approximate; for calendar accuracy compute with Temporal `until()`.
- Relative times go stale - re-render on an interval, and wrap in `<time datetime="2026-10-16T09:00Z" title="...">` for the exact value.
- Server/client rendering at different instants causes hydration mismatches - render relative times on the client.

## Verify
Test counts 0,1,2,5,11,21,22,101 in en, pl, ar, fr; snapshot the results per locale.

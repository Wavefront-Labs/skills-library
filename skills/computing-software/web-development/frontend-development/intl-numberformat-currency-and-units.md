---
id: computing-software.web-development.frontend-development.intl-numberformat-currency-and-units
name: intl-numberformat-currency-and-units
category: computing-software
field: web-development
product: frontend-development
tags: [intl-api, intl-numberformat, currency-formatting, units, i18n, javascript]
level: practitioner
status: verified
description: "Formatting numbers, currencies, percentages, units and compact values with Intl.NumberFormat, plus rounding, money storage and parsing traps."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat
  - https://tc39.es/ecma402/#numberformat-objects
  - https://www.iso.org/iso-4217-currency-codes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Intl.NumberFormat

## 1. Recipes
```js
const L = navigator.language;
new Intl.NumberFormat(L, { style: "currency", currency: "EUR" }).format(1234.5);      // "1.234,50 €" (de) / "€1,234.50" (en-IE)
new Intl.NumberFormat(L, { style: "currency", currency: "JPY" }).format(1234.5);      // "¥1,235" - 0 decimals for JPY
new Intl.NumberFormat(L, { style: "percent", maximumFractionDigits: 1 }).format(0.256); // "25.6%"
new Intl.NumberFormat(L, { notation: "compact" }).format(1_250_000);                   // "1.3M"
new Intl.NumberFormat(L, { style: "unit", unit: "kilometer-per-hour", unitDisplay: "short" }).format(50);
new Intl.NumberFormat(L, { signDisplay: "exceptZero" }).format(delta);                 // "+3", "-2", "0"
new Intl.NumberFormat(L, { style: "currency", currency: "USD", currencySign: "accounting" }).format(-5); // "($5.00)"
```
- `currency` is required with style currency; it decides the decimal count. Never hardcode symbols or `toFixed(2)` for display.
- `currencyDisplay: "code" | "name" | "narrowSymbol"` ("$" vs "US$" ambiguity): in `en-CA`, USD printed `US$5.00` (symbol), `USD 5.00` (code), `5.00 US dollars` (name) and `$5.00` (narrowSymbol). Omitting `currency` with `style: "currency"` throws `TypeError`.
- `formatRange(3, 5)`, `formatToParts()` for styling the symbol separately.

## 2. Money storage
Store integer minor units (cents) or decimal strings; floats lose precision (`0.1 + 0.2`). Format with `amount / 10 ** digits` only at display, or pass a string to `format("1234.567")` (ES2023 accepts strings for exact decimals). Use `roundingMode: "halfEven"` for banking rules (Node 20: `maximumFractionDigits: 0` formats 2.5 as `3` by default and `2` with `halfEven`; a string such as `"12345678901234567890.123"` printed exactly with `maximumFractionDigits: 20`).

## 3. Pitfalls
- Locale output contains non-breaking/narrow spaces (`fr-FR` currency printed U+202F in the group and U+00A0 before `€`; `de` printed U+00A0 before `€`) - snapshot tests comparing to `"1 234,50 €"` with a normal space fail. Normalise in tests.
- Output differs between ICU versions (Node vs browsers vs years) - do not assert exact strings across environments.
- Parsing localized input back is not provided. Use `formatToParts` to learn the locale's group/decimal symbols and strip/replace, or use `<input inputmode="decimal">` with explicit rules.
- Node built with `small-icu` (old/custom builds) only has English - check `Intl.NumberFormat.supportedLocalesOf(["de"])`.
- Cache formatters; creating one per table cell is slow.

## Verify
Unit tests over `["en-US","de-DE","fr-FR","ja-JP","ar-EG"]` with normalised whitespace.

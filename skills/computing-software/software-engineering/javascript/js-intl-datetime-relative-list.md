---
id: computing-software.software-engineering.javascript.js-intl-datetime-relative-list
name: js-intl-datetime-relative-list
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, intl-relativetimeformat, js-intl]
level: practitioner
status: docs-checked
description: "Format relative times such as yesterday or in 3 days with Intl.RelativeTimeFormat: options, formatToParts and locale support checks."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Intl.RelativeTimeFormat

- `new Intl.RelativeTimeFormat(locales, options)` then `rtf.format(value, unit)`. Negative values are in the past, positive in the future: with `"en"` defaults, `format(-1, "day")` is `"1 day ago"` and `format(1, "day")` is `"in 1 day"`.
- Options and their documented values: `localeMatcher` (`"best fit"` default, or `"lookup"`), `numeric` (`"always"` default, or `"auto"`), `style` (`"long"` default, or `"short"` or `"narrow"`).
- `numeric: "auto"` produces idiomatic words where the language has them: `"en"` gives `"yesterday"` for `-1` days, and `"es"` with `format(2, "day")` gives `"pasado mañana"`. `style: "short"` gives forms such as `"in 3 qtrs."` for `format(3, "quarter")`.
- `formatToParts(value, unit)` returns an array of parts for custom layout, for example literal `"in "`, integer `"100"` (with `unit: "day"`) and literal `" days"`.
- `resolvedOptions()` returns the locale and options actually computed; `Intl.RelativeTimeFormat.supportedLocalesOf(locales)` returns the locales supported without falling back to the runtime default.

Self-check: `new Intl.RelativeTimeFormat("en", { numeric: "auto" }).formatToParts(-1, "day")` is a single literal `"yesterday"`.

## Checked

Confirmed on the MDN Intl.RelativeTimeFormat page: constructor options and defaults, format and formatToParts outputs, the `es` and short-style examples, `resolvedOptions` and `supportedLocalesOf`. Removed: all `Intl.DateTimeFormat` and `Intl.ListFormat` claims (dateStyle, timeStyle, formatRange, conjunction lists), formatter caching advice, `navigator.languages`, IANA `timeZone` advice and the Node ICU note, none of which this page states. The skill now covers only RelativeTimeFormat, the one page it cites.

Method: docs-only read of cited pages, 2026-11-08

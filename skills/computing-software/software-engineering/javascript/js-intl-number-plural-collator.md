---
id: computing-software.software-engineering.javascript.js-intl-number-plural-collator
name: js-intl-number-plural-collator
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, intl-pluralrules, js-intl]
level: practitioner
status: docs-checked
description: "Choose plural and ordinal forms with Intl.PluralRules select and selectRange; categories zero to other and why n === 1 is not enough."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/PluralRules"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Intl.PluralRules

- `new Intl.PluralRules(locale, { type })` then `rules.select(n)` returns a plural-category tag; `selectRange(start, end)` does the same for a range. The possible tags are `zero`, `one`, `two`, `few`, `many` and `other` (`other` is the general form, also used when a language has only one form).
- Languages differ: English has two cardinal forms (`one` for 1, `other` for 0 and everything else), Chinese has one, Arabic has six. So do not hard-code `n === 1`; map each tag the language uses to a message.
- Cardinal is the default; `type: "ordinal"` selects ordinal rules. English ordinals use four tags: `one` (1st, 21st, 31st), `two` (2nd, 22nd), `few` (3rd, 33rd) and `other` (0th, 4th to 20th and so on). MDN's pattern is a `Map` from tag to suffix (`one` to `st`, `two` to `nd`, `few` to `rd`, `other` to `th`).
- The form depends on constructor options too, such as how the number is rounded, as well as on cardinal versus ordinal.
- Choosing the sentence is language specific: plural form can affect nouns, verbs and pronouns ("1 dog is happy", "10 dogs are happy"), and some English nouns (fish, sheep) do not change.
- Pass the application's UI language (and any fallbacks) as the constructor locales; `supportedLocalesOf()` and `resolvedOptions()` are available. The full per-language rules are in the Unicode LDML Language Plural Rules.

Self-check: `new Intl.PluralRules("ar-EG").select(0)` is `"zero"`, `select(6)` is `"few"` and `select(18)` is `"many"`; `new Intl.PluralRules("en-US", { type: "ordinal" }).select(21)` is `"one"`.

## Checked

Confirmed on the MDN Intl.PluralRules page: tag set, English and Arabic examples, ordinal rules and suffix map, options dependence and methods. Removed: all `Intl.NumberFormat` (currency, compact, units), `Intl.Collator` (sorting, `numeric`, `sensitivity`, Swedish ordering, `localeCompare` speed), `Intl.DisplayNames` and currency minor-unit claims, none of which this page states. The skill now covers only PluralRules, the one page it cites.

Method: docs-only read of cited pages, 2026-11-08

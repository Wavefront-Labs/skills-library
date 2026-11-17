---
id: computing-software.web-development.frontend-development.icu-messageformat-and-i18next
name: icu-messageformat-and-i18next
category: computing-software
field: web-development
product: frontend-development
tags: [icu-messageformat, i18next, formatjs, react-intl, translation-workflow, internationalization]
level: practitioner
status: verified
description: "Translation message workflow: ICU MessageFormat plural/select syntax, FormatJS/react-intl and i18next setups, extraction, translator context and pseudo-localisation."
sources:
  - https://formatjs.github.io/docs/core-concepts/icu-syntax
  - https://www.i18next.com/translation-function/plurals
  - https://unicode-org.github.io/icu/userguide/format_parse/messages/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ICU MessageFormat and i18next

## 1. Never concatenate
`t("You have") + n + t("messages")` cannot be translated: word order, plural forms (Polish has 4, Arabic 6) and gender differ. One message per sentence with placeholders.

## 2. ICU syntax (FormatJS/intl-messageformat, react-intl, Lingui; vue-i18n has its own message syntax)
```
{count, plural,
  =0 {No messages}
  one {# message from {sender}}
  other {# messages from {sender}}}
{gender, select, female {She replied} male {He replied} other {They replied}}
{place, selectordinal, one {#st} two {#nd} few {#rd} other {#th}}
Last seen {when, date, medium}
```
`other` is mandatory (omitting it throws `MISSING_OTHER_CLAUSE` in intl-messageformat). `#` is the locale-formatted number (`1234` printed `1,234`). Run with `intl-messageformat` the block above gave `No messages`, `1 message from Ann`, `2 messages from Ann`, ordinals `1st 2nd 3rd 4th 11th 21st 22nd 23rd`, and `Last seen Oct 18, 2026`. `Intl.PluralRules` categories: Polish `one,few,many,other` (4), Arabic `zero,one,two,few,many,other` (6), Russian 4, English 2.

```jsx
import { FormattedMessage, useIntl } from "react-intl";
<FormattedMessage id="inbox.count" defaultMessage="{count, plural, one {# message} other {# messages}}"
  description="Inbox header counter" values={{ count }} />
```
Extract: `formatjs extract "src/**/*.tsx" --out-file lang/en.json --id-interpolation-pattern "[sha512:contenthash:base64:6]"`; compile: `formatjs compile lang/fr.json --ast --out-file compiled/fr.json` (pre-parsed AST, smaller runtime; both commands ran with `@formatjs/cli`; `extract` keeps an explicit `id` such as `inbox.count`, the id pattern only generates missing ids).

## 3. i18next
```json
{ "inbox_one": "{{count}} message", "inbox_other": "{{count}} messages",
  "greeting": "Hello {{name}}" }
```
```js
i18next.t("inbox", { count: 3 });   // "3 messages": suffixes chosen with Intl.PluralRules (v21+ JSON format v4); Polish needs _one/_few/_many/_other keys
```
Use `i18next-icu` if you want ICU syntax; `react-i18next` `useTranslation()`/`<Trans>` for embedded markup; `i18next-parser` to extract keys; namespaces per feature with lazy loading (`i18next-http-backend`).

## 4. Workflow
- Source strings with **descriptions/context** for translators (button vs heading, max length).
- Stable keys; never reuse a key for a different meaning.
- TMS (Crowdin, Lokalise, Phrase) syncs JSON via CLI in CI; fail the build on missing keys in the default locale only.
- Pseudo-localise (`[Ŝéţţîñĝš___]`) in dev to catch hard-coded strings and 30-40% text expansion.

## Gotchas
- Escape literal braces/apostrophes in ICU: `'{'` and `''` (`It''s '{'x'}'` rendered `It's {x}`).
- HTML in messages: use rich-text tags (`<b>{name}</b>` with tag handlers), never `dangerouslySetInnerHTML` on translations.
- Load only the active locale's messages; bundling all locales bloats JS.

## Verify
- [ ] Pseudo-locale build shows no untranslated English.
- [ ] Plural tests for 0, 1, 2, 5, 21 in a language like Polish or Russian.

---
id: computing-software.web-development.frontend-development.input-types-and-mobile-keyboards
name: input-types-and-mobile-keyboards
category: computing-software
field: web-development
product: frontend-development
tags: [html-forms, input-types, inputmode, enterkeyhint, mobile-keyboard, type-email, type-tel, type-number, autocapitalize, spellcheck, forms]
level: practitioner
status: docs-checked
description: "Choosing HTML input types plus inputmode/enterkeyhint/autocapitalize so mobile users get the right keyboard without breaking validation or paste."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inputmode
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/pattern
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Input types and mobile keyboards

**Goal:** every field shows the right on-screen keyboard, validates sensibly, and still accepts paste and autofill.

## 1. Choose `type` by data semantics, not by keyboard
| Data | Markup | Why |
|---|---|---|
| Email | `type="email" autocomplete="email"` | `@` keyboard + built-in format check |
| Phone | `type="tel" autocomplete="tel"` | Dial pad; no format validation (phone formats vary) |
| URL | `type="url"` | Valid only as `scheme://rest-of-url` (the scheme need not exist) |
| Search box | `type="search"` + `enterkeyhint="search"` | "Search" return key |
| Quantity / age | `type="number" min max step` | Spinner; value is a number |
| Card number, PIN, OTP, postcode, ID numbers | `type="text" inputmode="numeric" pattern="[0-9]*"` | **Not** `type="number"` |
| Date | `type="date"` (or three text fields for birth dates) | Native picker, value is `YYYY-MM-DD` |

**Never use `type="number"` for things that are not quantities.** MDN says `number` suits incremental values where a spinbutton helps, and is not appropriate for numeric-looking values such as credit card numbers or postcodes. Those are strings of digits.

## 2. `inputmode` = keyboard only
`inputmode` changes the virtual keyboard without changing validation or the value type: `none | text | decimal | numeric | tel | search | email | url`. Use `decimal` for prices (shows `.`/`,` per locale), `numeric` for digit strings.

## 3. Return key and casing
- `enterkeyhint="next|done|go|send|search|previous|enter"` labels the return key. It is a hint only; you still handle focus moves yourself.
- `autocapitalize="off"` and `spellcheck="false"` on usernames, emails, codes; `autocapitalize="words"` on names.
- `autocorrect="off"` on codes and usernames.

## 4. Gotchas
- `pattern` is anchored implicitly (`^(?:pattern)$`) and is compiled with the `v` flag, so `(`, `)`, `[`, `{`, `}`, `/`, `-` and `|` must be escaped when literal inside character classes (`[\w\-]`); the pattern attribute applies only to text, tel, email, url, password and search inputs.
- `type="email"` accepts `a@b` (no TLD) - that is spec-valid; do real verification by sending mail.

## Verify
- [ ] On a real iOS and Android device each field opens the expected keyboard.
- [ ] Pasting a formatted card number (`4242 4242 …`) works (strip spaces in JS, do not block).
- [ ] Digit-string fields (cards, postcodes) use `type="text"` with `inputmode`, not `type="number"`.

## Checked
2026-10-26. MDN inputmode, enterkeyhint, autocorrect, pattern and input type pages (main, 2026-10-26): confirmed the inputmode keywords (none, text, decimal, numeric, tel, search, email, url), pattern must match the whole value and is compiled with the v flag (literal ( ) [ { } / - | need escaping in classes) and applies to text, tel, email, url, password and search, tel has no format validation, url needs scheme://rest, email accepts username@domain, date value normalises to yyyy-mm-dd, and number is not for card or postcode style values. Removed the iOS 16px zoom rule, the maxlength truncation claim, the Safari-only autocorrect note, the search clear button and the number-input behaviour list, none of which a fetched page confirms.
Method: documentation only; no commands were run.

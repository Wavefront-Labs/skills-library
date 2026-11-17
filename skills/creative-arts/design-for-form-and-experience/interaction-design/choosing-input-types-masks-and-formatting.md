---
id: creative-arts.design-for-form-and-experience.interaction-design.choosing-input-types-masks-and-formatting
name: choosing-input-types-masks-and-formatting
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [input-masks, input-types, input-formatting, autocomplete-attributes, mobile-keyboards, form-design, data-entry]
level: practitioner
status: draft
description: "Choose the right input type, inputmode and autocomplete values, accept flexible formats rather than strict masks, and format on blur for phone, card and date fields."
sources:
  - "MDN Web Docs - input element types, inputmode and autocomplete (developer.mozilla.org/docs/Web/HTML/Element/input)"
  - "WHATWG HTML Standard - autofill field names (html.spec.whatwg.org/multipage/form-control-infrastructure.html#autofill)"
  - "Baymard Institute - Form field input masks and formatting (baymard.com/blog)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Input types, masks and formatting

**Goal:** the right keyboard, autofill and format handling so entry is fast and forgiving.

## Types and keyboards
- `type="email"`, `tel`, `url`, `search`, `password`, `number` (for quantities; not for postcodes, card numbers or phone numbers: leading zeros and spinners are harmful), `date` (native picker for known dates; consider three fields for birthdays).
- `inputmode="numeric"` with `pattern="[0-9]*"` for codes and card numbers; `inputmode="decimal"` for amounts; `enterkeyhint="next|done|search"`.
- Set `autocapitalize="off"` and `autocorrect="off"` on emails and usernames.

## Autofill
Use standard `autocomplete` tokens: `name`, `given-name`, `family-name`, `email`, `tel`, `street-address`, `postal-code`, `cc-number`, `cc-exp`, `one-time-code`, `new-password`, `current-password`. Correct tokens let browsers and password managers fill the form.

## Masks and formatting
- Prefer **accepting flexible input** and normalising it (spaces or dashes in phone and card numbers) over rigid masks that block pasting and fight the cursor.
- If you use a mask, preserve caret position, allow paste and deletion, and show the format in hint text (`creative-arts.design-for-form-and-experience.interaction-design.writing-form-labels-placeholders-and-help-text`).
- Format on blur (add spaces to card number groups, format phone with libphonenumber) and strip on submit.
- Use `maxlength` carefully (it silently truncates); validate length instead.
- Do not require one country's format for names, phone numbers or addresses; allow international values.

## Verify
- [ ] Each field has the right type, inputmode and autocomplete.
- [ ] Paste and autofill work; no rigid mask blocks valid values.
- [ ] Tested on iOS and Android keyboards.

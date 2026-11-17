---
id: computing-software.ux-hci-design.interaction-design.form-input-types-and-autofill
name: form-input-types-and-autofill
category: computing-software
field: ux-hci-design
product: interaction-design
tags: [input-types-inputmode, autocomplete-attribute]
level: practitioner
status: draft
description: "Choose correct HTML input types, inputmode and autocomplete tokens for faster mobile entry."
sources:
  - https://html.spec.whatwg.org/multipage/forms.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Input choices
- `type="email|tel|url|number|date"` choose the right mobile keyboard. `type=number` is poor for IDs, card or phone numbers (spinners, drops leading zeros): use `inputmode="numeric"` with `pattern`.
- `autocomplete` tokens: `username`, `current-password`, `new-password`, `one-time-code`, `name`, `email`, `street-address`, `cc-number`.
- `autocapitalize`, `enterkeyhint` for mobile polish.
- Do not block paste.

## Verify
- [ ] On a phone, the right keyboard appears and autofill offers saved data.

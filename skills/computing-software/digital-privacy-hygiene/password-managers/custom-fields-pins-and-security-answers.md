---
id: computing-software.digital-privacy-hygiene.password-managers.custom-fields-pins-and-security-answers
name: custom-fields-pins-and-security-answers
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, custom-fields, hidden-fields, security-answer-storage, account-pin, verbal-password, linked-fields, autofill]
level: practitioner
status: draft
description: "Store per-account PINs, verbal passwords, random security answers and account numbers as typed custom fields on the login item, hidden and fillable where useful."
sources:
  - "https://bitwarden.com/help/custom-fields/"
  - "https://support.1password.com/custom-fields/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom fields for PINs and security answers

**Goal:** every secret tied to an account lives on that account's item, so you can
answer a phone verification or a security question without hunting.

## Field types (Bitwarden names; 1Password has equivalents)
- **Text**: account number, customer ID (not secret but needed).
- **Hidden**: PINs, verbal passwords, security answers. Masked on screen and
  excluded from some views.
- **Boolean**: checkbox fills.
- **Linked**: map a page field (e.g. `memorable_word`) to the item's password/username.

## Conventions that scale
Name fields so search and phone calls work:
- `Phone PIN` (carrier port-out PIN, bank telephone PIN)
- `Verbal password`
- `SQ: first pet` -> value `blue-anchor-74` (random answer; see
  `computing-software.digital-privacy-hygiene.password-hygiene.random-answers-to-security-questions`)
- `Account no.`

## Autofill of custom fields
Bitwarden fills custom fields whose **name matches the HTML field's id, name, label
or placeholder**. Inspect the page field (right-click > Inspect) and set the custom
field name to its `name` attribute to make it fill. Bank "enter characters 2, 5 and 7
of your memorable word" forms can't be autofilled; reveal and type.

## Gotchas
- Some exports flatten hidden fields to plain text; treat exports as plaintext.
- Don't put a secret in the **Notes** field when it belongs in a hidden field; notes are
  shown unmasked.

## Verify
- [ ] Carrier, bank and email items each hold their PIN / verbal password as hidden fields.
- [ ] A test custom field autofills on a page by name match.

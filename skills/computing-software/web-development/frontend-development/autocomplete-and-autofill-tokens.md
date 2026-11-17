---
id: computing-software.web-development.frontend-development.autocomplete-and-autofill-tokens
name: autocomplete-and-autofill-tokens
category: computing-software
field: web-development
product: frontend-development
tags: [html-forms, autocomplete-attribute, autofill-tokens, password-manager, one-time-code, input-purpose, address-autofill, webauthn-autocomplete]
level: practitioner
status: docs-checked
description: "Using autocomplete tokens (name, address, cc, current/new-password, one-time-code) so browsers and password managers fill forms correctly."
sources:
  - https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#autofill
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/autocomplete
  - https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/Turning_off_form_autocompletion
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autocomplete and autofill tokens

**Goal:** browsers and password managers fill every field correctly on first try (also satisfies WCAG 1.3.5 Identify Input Purpose).

## 1. The tokens that matter
| Field | Token |
|---|---|
| Full name / given / family | `name`, `given-name`, `family-name` |
| Email, phone | `email`, `tel` (`tel-national` if you strip country code) |
| Address | `street-address` (textarea) or `address-line1`/`address-line2`, `address-level2` (city), `address-level1` (state), `postal-code`, `country` / `country-name` |
| Card | `cc-name`, `cc-number`, `cc-exp` (or `cc-exp-month`/`cc-exp-year`), `cc-csc` |
| Login | `username`, `current-password` |
| Sign-up / change password | `new-password` |
| SMS code | `one-time-code` |
| Passkey conditional UI | `autocomplete="username webauthn"` (`webauthn` must be the last token) |
| Birthday | `bday`, `bday-day`, `bday-month`, `bday-year` |

Sections and groups: prefix `shipping` / `billing` (`autocomplete="shipping postal-code"`) and `section-<name>` for repeated blocks.

## 2. Login forms password managers understand
```html
<form method="post" action="/login">
  <label>Email <input name="email" type="email" autocomplete="username" required></label>
  <label>Password <input name="password" type="password" autocomplete="current-password" required></label>
  <button>Sign in</button>
</form>
```
- Use a real `<form>` with a submit button; managers watch form submission and navigation.
- Don't block paste in password fields.

## 3. `autocomplete="off"`
Most modern browsers do not honour `autocomplete="off"` on login fields: a password manager can still offer to save and fill them. See the MDN guide on turning off form autocompletion before relying on `off` anywhere.

## 4. One-time codes
`<input inputmode="numeric" autocomplete="one-time-code" pattern="\d{6}">` lets iOS/Android offer the SMS code.

## Verify
- [ ] Chrome and Safari autofill fill every address/card field in one click with no wrong-field values.
- [ ] Password manager offers to save on sign-up and fills on login.
- [ ] Lighthouse / axe report no `autocomplete` violations.

## Checked
2026-10-26. MDN autocomplete attribute page and the turning-off-autocompletion guide (main, 2026-10-26): confirmed the token names used (name, given-name, family-name, email, tel, tel-national, street-address, address-line1/2, address-level1/2, postal-code, country, country-name, cc-name, cc-number, cc-exp, cc-exp-month/year, cc-csc, username, current-password, new-password, one-time-code, bday, bday-day/month/year), the optional section-* then shipping/billing grouping order, that the webauthn token goes last, and that modern browsers do not honour off for login fields. Removed the SMS domain-binding format, the hidden-username advice and the new-password-to-block-autofill advice, which no fetched page confirms.
Method: documentation only; no commands were run.

---
id: computing-software.web-development.web-accessibility.error-identification-and-suggestions
name: error-identification-and-suggestions
category: computing-software
field: web-development
product: web-accessibility
tags: [input-assistance, accessible-forms, error-identification, error-suggestion, wcag-3-3-1, wcag-3-3-3, aria-invalid, inline-errors, error-messages]
level: practitioner
status: docs-checked
description: "Meeting WCAG 3.3.1 and 3.3.3: identifying errors in text, linking messages with aria-describedby and aria-invalid, and writing messages that say how to fix."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html
  - https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error identification and suggestions

**Goal:** when input is wrong, every user learns which field, what's wrong and how to fix it.

## 1. Identify in text (3.3.1, A)
Red borders alone fail (colour only, and not announced). Each invalid field needs a text message, programmatically associated:
```html
<label for="dob-year">Year</label>
<p id="dob-error" class="error"><span class="visually-hidden">Error:</span> Year must include 4 numbers</p>
<input id="dob-year" inputmode="numeric" aria-invalid="true" aria-describedby="dob-hint dob-error">
```
- `aria-invalid="true"` only after validation fails (not on page load for empty required fields).
- Put the message next to the field in error (the Understanding page shows messages beside the specific fields) and keep it visible until fixed. Colour or an icon may be added in addition to the text but not instead of it.
- An "Error:" prefix (visually hidden or visible icon with alt) helps when colour isn't perceived.

## 2. Suggest the fix (3.3.3, AA)
| Vague | Helpful |
|---|---|
| "Invalid input" | "Enter a date in the past, like 27 3 2007" |
| "Required" | "Enter your postcode" |
| "Error 422" | "That email is already registered - sign in or reset your password" |
| "Password invalid" | "Password must be at least 12 characters" |
Unless the suggestion would compromise security (don't reveal which of username/password was wrong).

## 3. Server-side errors
Return field-level errors (for example as extension members of an RFC 9457 problem details object) so the UI can attach them to fields, not only one banner.

## 4. Timing
Validate on submit (and optionally on blur after first interaction); don't show errors while the user is still typing the first time. Remove the message and `aria-invalid` as soon as it's fixed.

## Verify
- [ ] Each error message is read by the screen reader when focusing its field (check accessibility pane "Description").
- [ ] Errors understandable in greyscale.
- [ ] Every message says how to fix the problem.

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text: 3.3.1 Error Identification is Level A (item in error identified and described in text) and 3.3.3 Error Suggestion is Level AA (suggestions unless they would jeopardize the security or purpose of the content); the Understanding page allows colour or icons in addition to text and messages next to the fields. Removed the unconfirmed mobile-keyboard and browse-mode placement claims and the GOV.UK source.

Method: documentation only; no commands were run.

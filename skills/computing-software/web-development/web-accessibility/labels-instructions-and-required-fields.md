---
id: computing-software.web-development.web-accessibility.labels-instructions-and-required-fields
name: labels-instructions-and-required-fields
category: computing-software
field: web-development
product: web-accessibility
tags: [input-assistance, accessible-forms, labels-or-instructions, required-fields, wcag-3-3-2, hint-text, format-instructions, optional-fields]
level: practitioner
status: docs-checked
description: "Meeting WCAG 3.3.2 Labels or Instructions: visible labels, format hints before input, marking required/optional fields and instructions screen readers get."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html
  - https://www.w3.org/WAI/tutorials/forms/instructions/
  - https://design-system.service.gov.uk/patterns/question-pages/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Labels, instructions and required fields

**Goal:** users know what to enter and in what format before they make a mistake.

## 1. Visible labels for every input (3.3.2, A)
- Persistent visible label; placeholder text is not a replacement for labels (assistive technology does not treat it as one, and its contrast is often too low).
- Groups (date of birth, phone with country code) need a group label (`fieldset/legend`) plus per-field labels ("Day", "Month", "Year").

## 2. Instructions before the field
```html
<label for="ref">Booking reference</label>
<div id="ref-hint" class="hint">8 characters, found in your confirmation email, like AB12CD34</div>
<input id="ref" aria-describedby="ref-hint" autocomplete="off">
```
- Format requirements (date format, password rules, allowed file types/sizes) stated up front, not only in error messages.
- Form-level instructions ("All fields are required unless marked optional") go **before** the form, not after the submit button.
- Accept flexible input instead of instructing (strip spaces/dashes from card and phone numbers; accept "1/2/2026" and "01/02/2026").

## 3. Required vs optional
- Native `required` attribute (announced as "required") plus a visible marker.
- The GOV.UK Design System adds "(optional)" to the labels of optional fields and says never to mark mandatory fields with asterisks.
- If you use asterisks, explain them at the top and make sure the asterisk isn't the only cue for screen readers (the `required` attribute exposes the state).

## 4. Don't rely on sensory/position cues
"Fill in the fields on the right" or "fields in green" fail 1.3.3.

## Verify
- [ ] Every input has a visible label that remains visible while typing.
- [ ] Screen reader reads label, hint and required state on focus.
- [ ] Format hints exist for any field with a format rule.

## Checked

- Date: 2026-10-26. Documentation: WCAG 2.2 3.3.2, WAI Forms tutorial (instructions), GOV.UK Design System question pages pattern.
- Confirmed: 3.3.2 is Level A; overall form instructions go before the form; format hints belong in the label or beside the field; placeholder text is not a substitute for a label; optional fields marked "(optional)" and no asterisks for mandatory fields (GOV.UK).
- Removed (no documentation found): the floating-label allowance and the `aria-required` and `novalidate` advice.
Method: documentation only; no commands were run.
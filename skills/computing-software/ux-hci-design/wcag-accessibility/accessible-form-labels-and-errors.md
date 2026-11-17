---
id: computing-software.ux-hci-design.wcag-accessibility.accessible-form-labels-and-errors
name: accessible-form-labels-and-errors
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [accessible-form-errors, error-identification, wcag-input-assistance]
level: practitioner
status: gated
description: "Label every field, identify errors in text, associate messages programmatically and suggest corrections."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html
  - https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Form errors (SC 3.3.1 A, 3.3.2 A, 3.3.3 AA)
```html
<label for="e">Email</label>
<input id="e" type="email" aria-invalid="true" aria-describedby="e-err" required>
<p id="e-err">Enter an email like name@example.com.</p>
```
- Describe the error in text and identify the field.
- Error summary at top linking to fields; move focus to it on failed submit.
- Mark required fields in text (not only asterisks without explanation).
- Do not use `placeholder` as the label.

## Verify
- [ ] Screen reader announces label, required and error for each field.

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; Understanding SC 3.3.1 and 3.3.2 were fetched but 3.3.3, the error-summary/focus advice, required-field marking and placeholder advice are not on them. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.

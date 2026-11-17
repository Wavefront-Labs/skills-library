---
id: computing-software.ux-hci-design.wcag-accessibility.orientation-and-input-purpose
name: orientation-and-input-purpose
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [identify-input-purpose, orientation-wcag]
level: practitioner
status: docs-checked
description: "Do not lock orientation and mark personal-data fields with autocomplete tokens (SC 1.3.4 and 1.3.5)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/identify-input-purpose.html
  - https://www.w3.org/WAI/WCAG22/Understanding/orientation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 1.3.4 Orientation (AA) and 1.3.5 Identify Input Purpose (AA)
- 1.3.4 (AA): do not restrict content view and operation to a single display orientation (portrait or landscape) unless a specific orientation is essential. Examples of essential: a bank check, a piano app.
- 1.3.5 (AA): identify the purpose of input fields about the user. The HTML `autocomplete` attribute accepts only a fixed list of values, for example `name`, `given-name`, `family-name`, `username`, `nickname`, `bday`, `tel`.
```html
<input id="gn" name="gn" autocomplete="given-name">
```
- `type="email"` or `type="tel"` alone does not say whose email or phone the field is, so also add the `autocomplete` value.

## Verify
- [ ] Rotate device: nothing disappears and operation still works in both orientations.

## Checked

- Date: 2026-11-09.
- Confirmed against Understanding SC 1.3.4 Orientation and Understanding SC 1.3.5 Identify Input Purpose (both Level AA): the orientation exception and essential examples, the autocomplete attribute, and the tokens `name`, `given-name`, `family-name`, `username`, `nickname`, `bday`, `tel`. Pages were searched for these claims rather than read line by line.
- Removed: the tokens `email`, `street-address`, `postal-code`, `cc-number` (not confirmed on the pages), the link to 3.3.7 and the autofill check.

Method: documentation only; no commands were run.

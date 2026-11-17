---
id: computing-software.ux-hci-design.wcag-accessibility.predictable-focus-and-input
name: predictable-focus-and-input
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [on-input, context-change]
level: practitioner
status: docs-checked
description: "Do not change context when a control's setting changes unless users were warned first (SC 3.2.2 On Input)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/on-input.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Predictability
- SC 3.2.2 (Level A): changing the setting of any user interface component must not automatically cause a change of context unless the user was told the behaviour before using the component.
- Changes of context include a change of user agent, viewport, focus, or content that changes the meaning of the page (new window, focus moved elsewhere, a new page, major rearrangement). A change of content alone is not a change of context.
- Changing a setting means ticking a checkbox, typing in a text field or choosing a different option; activating a link or button is not a setting change.
- Sufficient techniques: a submit button to start the change (G80, H32), or describing what will happen before the control is changed (G13).
- Failures: automatically submitting a form once a field is given a value (F36); launching a new window without warning when a radio button, check box or select is changed (F37).
- Allowed with a warning: a phone number split into several fields that auto-advances focus, if the behaviour is described at the start of the form.

## Verify
- [ ] Tab through all fields and change values: no unexpected navigation.

## Checked

- Date: 2026-11-09.
- Read Understanding SC 3.2.2 On Input (Level A): the criterion text, intent notes on buttons, examples, sufficient techniques and failures F36/F37, and the change-of-context definition.
- Removed: the on-focus (3.2.1) claims, which the cited page does not cover, the "prefer Go button over onchange" absolute and the OTP advice.

Method: documentation only; no commands were run.

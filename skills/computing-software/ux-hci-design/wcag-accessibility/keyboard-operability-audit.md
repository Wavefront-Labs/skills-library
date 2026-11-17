---
id: computing-software.ux-hci-design.wcag-accessibility.keyboard-operability-audit
name: keyboard-operability-audit
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [keyboard-operability, keyboard-trap, wcag-keyboard]
level: practitioner
status: docs-checked
description: "Test that every function works by keyboard alone and that focus can always leave a component (SC 2.1.1, 2.1.2)."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html
  - https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyboard audit (SC 2.1.1 and 2.1.2, both Level A)
1. Unplug the mouse and operate the page by keyboard only. Operation must not require specific timings for individual keystrokes.
2. All functionality must be operable by keyboard, except where the function depends on the path of the movement (freehand drawing). Dragging an object to a location is not path-dependent, so offer another route such as cut and paste or form controls.
3. Not every control must be focusable if a comparable keyboard route exists. Following platform key conventions is best practice but not required (a custom button that reacts only to Enter still passes).
4. No trap: focus can leave a component using unmodified arrow keys, Tab or another standard exit method; if another key is needed the user must be told. A modal dialog may restrict focus if it can be dismissed (Cancel, OK or the Esc key).

## Common failures
Controls that only work with a pointer; drag-only interactions with no alternative. Native HTML form controls and links give keyboard control (H91). MouseKeys does not satisfy 2.1.1.

## Verify
- [ ] Complete the main user journey with keyboard alone.

## Checked

- Date: 2026-11-09.
- Read Understanding SC 2.1.1 Keyboard (criterion, intent, notes, examples, techniques) and searched Understanding SC 2.1.2 No Keyboard Trap for the modal dialog, standard exit methods and Level A claims.
- Removed: SC 2.4.3, tab-order and positive `tabindex` advice, Enter/Space and arrow-key rules, "return focus", `div onclick` and hover-only menu claims (not on the cited pages).

Method: documentation only; no commands were run.

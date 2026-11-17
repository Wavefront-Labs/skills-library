---
id: computing-software.web-development.web-accessibility.no-keyboard-trap
name: no-keyboard-trap
category: computing-software
field: web-development
product: web-accessibility
tags: [keyboard-accessibility, keyboard-trap, wcag-2-1-2, focus-management, embeds]
level: practitioner
status: docs-checked
description: "Preventing keyboard traps (WCAG 2.1.2): common sources like embeds, editors and custom widgets, distinguishing them from correct modal focus containment, and testing."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html
  - https://www.w3.org/WAI/WCAG22/Techniques/failures/F10
  - https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# No keyboard trap

**2.1.2 (A):** if focus can move into a component with the keyboard, it can move out with the keyboard using standard keys (Tab, Shift+Tab, arrows, Escape) - or the user is told how. This is one of the "non-interference" criteria: a failure blocks the whole page, even content that otherwise conforms.

## 1. Typical traps
- Embedded third-party iframes, plugins and widgets that swallow Tab.
- Rich text editors and code editors that use Tab to indent - need an escape route, and the SC allows a non-standard exit only if the user is advised of the method.
- Custom widgets that `preventDefault()` on all keydown events.
- Focus loops in carousels or "infinite" lists that re-focus the first item on blur.
- Modals that trap focus but provide **no** close via keyboard (no Escape, close button not focusable).
- JavaScript that moves focus back on `blur` (validation that re-focuses an invalid field).

## 2. Modals are not traps
A modal dialog should contain focus while open - that's correct, as long as Escape and a focusable Close button exit it and focus returns to the trigger. A native `<dialog>` opened with `showModal()` closes on Escape (MDN); make sure focus returns to the trigger afterwards.

## 3. Implementation rules
- Only intercept Tab when you also handle Shift+Tab and an exit path.
- Capture Tab in editors only after a deliberate "edit mode" entry, with Escape to leave.
- Third-party embeds: test before adopting; wrap with skip links ("Skip map") so users can bypass.
- Don't use `onblur` to force focus back.

## Verify
Unplug the mouse. Tab from the top of the page to the bottom and back with Shift+Tab, entering every widget, editor, iframe and dialog; you must always be able to leave. Record any non-standard exit keys in on-page instructions.

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text of 2.1.2 (Level A): focus must be movable away using only a keyboard interface, and if it needs more than unmodified arrow or tab keys or other standard exit methods the user is advised; all content on the page must meet it (the non-interference requirement). MDN confirms Escape closes a modal dialog. Removed the unconfirmed CodeMirror/Monaco key claims.

Method: documentation only; no commands were run.

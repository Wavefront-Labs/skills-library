---
id: computing-software.web-development.web-accessibility.pointer-cancellation-up-event
name: pointer-cancellation-up-event
category: computing-software
field: web-development
product: web-accessibility
tags: [input-modalities, pointer-accessibility, pointer-cancellation, wcag-2-5-2, up-event-activation, click-vs-mousedown, abort-activation]
level: practitioner
status: docs-checked
description: "Meeting WCAG 2.5.2 Pointer Cancellation: activating on the up-event (click) not pointerdown, allowing abort by moving away, and safe drag-and-drop patterns."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/pointer-cancellation.html
  - https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pointer cancellation (activate on up-event)

**Goal:** users who press the wrong target by accident can slide off before releasing and nothing happens.

## 1. The rule (2.5.2, A)
For single-pointer actions, at least one holds:
- **No down-event**: the down-event doesn't execute anything;
- **Abort or undo**: completes on the up-event and moving off the target before release aborts, or there's an undo;
- **Up reversal**: up-event reverses what down did (press-and-hold to preview, release hides);
- **Essential**: completing on the down-event is essential; functions that emulate a keyboard or numeric keypad key press count as essential.

## 2. In practice
- Use `click` (fires after pointer down **and** up on the same element - native abort behaviour) for activation. Don't trigger navigation, submission, deletion or purchase on `mousedown`, `pointerdown` or `touchstart`.
- Custom components that act on `onPointerDown`/`onMouseDown` "to feel faster" are a typical source of failures.
- If you need instant feedback, show a pressed state on down and do the action on up.

```js
// Bad
el.addEventListener('pointerdown', deleteItem);
// Good
el.addEventListener('click', deleteItem);
```

## 3. Drag and drop
Starting a drag on down is fine; the **drop** (the action) should happen on up and be abortable (for example by dropping outside a valid target). Provide a non-drag alternative anyway (2.5.7).

## 4. Menus that open on mousedown
Opening a menu on down is OK only if releasing outside does nothing harmful and selection happens on up. Selecting an item on down fails.

## Verify
- [ ] Press on each control, move the pointer off, release: nothing activates.
- [ ] Grep for `onMouseDown`/`onPointerDown`/`touchstart` handlers that perform actions.
- [ ] Destructive actions have confirmation or undo.

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text of 2.5.2 (Level A): the four options (no down-event, abort or undo, up reversal, essential) and that keyboard or keypad emulation is essential; MDN confirms click fires after both mousedown and mouseup on the element. Removed the piano example and the unconfirmed native-element claim.

Method: documentation only; no commands were run.

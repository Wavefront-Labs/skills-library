---
id: computing-software.web-development.frontend-development.native-dialog-details-and-popover
name: native-dialog-details-and-popover
category: computing-software
field: web-development
product: frontend-development
tags: [semantic-html, html-dialog-element, popover-api, details-summary, dialog, accessibility, top-layer]
level: practitioner
status: docs-checked
description: "Using native dialog (showModal), details/summary and the popover attribute instead of custom JS: focus handling, light dismiss, styling ::backdrop, and browser caveats."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog
  - https://developer.mozilla.org/en-US/docs/Web/API/Popover_API/Using
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details
  - https://html.spec.whatwg.org/multipage/interactive-elements.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Native dialog, details and popover

## 1. Modal `<dialog>`
```html
<button id="open">Delete project</button>
<dialog id="confirm" aria-labelledby="confirm-title">
  <form method="dialog">
    <h2 id="confirm-title">Delete project?</h2>
    <p>This cannot be undone.</p>
    <button value="cancel" autofocus>Cancel</button>
    <button value="delete">Delete</button>
  </form>
</dialog>
<script>
  const d = document.getElementById("confirm");
  open.onclick = () => d.showModal();
  d.addEventListener("close", () => { if (d.returnValue === "delete") deleteProject(); });
</script>
```
- `showModal()` puts it in the top layer, makes the rest of the page inert, shows the `::backdrop`, and Esc closes it; focus starts on the `autofocus` element or the first focusable element.
- `show()` opens a non-modal dialog (no inertness).
- `form method="dialog"` closes and sets `returnValue` to the button's `value`.
- Style the backdrop with `dialog::backdrop`. Prevent background scroll: `body:has(dialog[open]) { overflow: hidden }`.
- Light dismiss on backdrop click is not built in for modal dialogs (the `closedby="any"` attribute, Chrome 134 and Firefox 141, Safari preview); otherwise check `event.target === dialog` on click.
- Do not set `open` attribute directly for modals - that skips modality.

## 2. `<details>`/`<summary>`
```html
<details name="faq"><summary>Shipping times</summary><p>2-4 working days.</p></details>
```
- `name` groups several `<details>` so only one is open at a time (Chrome 120, Firefox 130, Safari 17.2). The `toggle` event fires when the state changes.

## 3. Popover attribute
```html
<button popovertarget="menu">Options</button>
<div id="menu" popover>…</div>
```
- `popover` (= `auto`) gives top layer, light dismiss (outside click, Esc), generally closes other non-nested auto popovers, and an invoker set with `popovertarget` gets implicit `aria-expanded` and `aria-details`. `popover="manual"` popovers are not light dismissed and must be closed explicitly (for toasts).
- Popover is not modal and does not trap focus; it is for menus, tooltips-on-click, pickers. Pair with CSS anchor positioning for placement.
- Animate entry with `@starting-style` and `transition-behavior: allow-discrete` on `display` and `overlay`.

## 4. Support
dialog: Chrome 37, Firefox 98, Safari 15.4. For popover, web-features carries a note (2024-09-18) that an iOS Safari bug prevents dismissing popovers by touch, so test on iOS; check the current support tables before dropping a fallback.

## Verify
- Keyboard: Tab never leaves an open modal; Escape closes; focus returns to the trigger.
- A screen reader announces the dialog with its name when opened.

## Checked
2026-10-26. MDN dialog, details, global popover attribute and Popover API using pages, browser-compat-data and web-features (main, 2026-10-26): confirmed showModal renders a backdrop, makes the rest inert and is removed from the top layer on close, Esc closes modals, form method=dialog sets returnValue, closedby values and support versions, details name grouping and support versions, popover auto versus manual behaviour, implicit aria-expanded, and transition-behavior allow-discrete with @starting-style and overlay. Removed focus-trap, cancel-then-close order, focus-return, find-in-page, Baseline 2024 popover, and polyfill claims that no fetched page confirms.
Method: documentation only; no commands were run.

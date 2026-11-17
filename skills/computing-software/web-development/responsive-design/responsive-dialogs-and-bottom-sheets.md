---
id: computing-software.web-development.responsive-design.responsive-dialogs-and-bottom-sheets
name: responsive-dialogs-and-bottom-sheets
category: computing-software
field: web-development
product: responsive-design
tags: [bottom-sheet, responsive-dialog, native-dialog, mobile-ui, responsive-design]
level: practitioner
status: verified
description: "Building a dialog that is centred on desktop and a bottom sheet on mobile with native dialog: CSS positioning, safe areas, scroll locking, drag to dismiss and focus handling."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog
  - https://web.dev/articles/building/a-sidenav-component
  - https://m3.material.io/components/bottom-sheets/guidelines
  - https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responsive dialogs and bottom sheets

One component, two presentations: a centred modal on wide screens, a sheet anchored to the bottom on narrow ones. Use native `<dialog>` with `showModal()` for focus trapping, Esc handling and inert background for free (run: focus moved to the first button, Tab left the page unreachable, Esc closed it and focus returned to the opener).

## 1. CSS
```css
dialog.sheet { border: 0; padding: 0; max-inline-size: min(36rem, 100% - 2rem); max-block-size: min(80dvh, 100% - 2rem);
               border-radius: 12px; overflow: auto; overscroll-behavior: contain; }
dialog.sheet::backdrop { background: rgb(0 0 0 / .4); }

@media (width < 40rem) {
  dialog.sheet { margin: auto 0 0; inline-size: 100%; max-inline-size: 100%; max-block-size: 90dvh;
                 border-radius: 16px 16px 0 0; padding-bottom: env(safe-area-inset-bottom); }
}
@media (prefers-reduced-motion: no-preference) {
  dialog.sheet[open] { animation: slide-up .25s ease-out; }
  @keyframes slide-up { from { translate: 0 100%; } }
}
```
- `margin: auto 0 0` pins the modal dialog to the bottom (dialogs are positioned with `inset: 0; margin: auto`; run: at 390px wide the dialog box spanned x 0-390 and y 678-800 in an 800px viewport, while at 1000px it was centred).
- Use `dvh` so the sheet respects mobile browser toolbars; add `viewport-fit=cover` to the viewport meta for safe-area values.
- `overscroll-behavior: contain` prevents scroll chaining into the page. A modal dialog does not lock page scrolling by itself: in Chromium 156 a mouse wheel over the backdrop scrolled the page (scrollY 500) and PageDown scrolled it (525) with a modal open; adding `html:has(dialog[open]) { overflow: hidden; }` stopped both (scrollY stayed 0). Keep that rule.

## 2. Behaviour
```js
dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); }); // tap backdrop
// closedby="any" (Chrome 134+, Firefox 141+ per MDN compat data) does light dismiss natively (run in Chromium 156: a backdrop click closed the dialog)
```
- A visible close button is required; drag-to-dismiss and backdrop tap are extras (WCAG 2.5.7 needs a single-pointer alternative to dragging).
- Drag handle: track `pointerdown/move/up` on the handle only, translate the sheet, close past ~30% height or a fast flick; respect `touch-action: none` on the handle.
- Put the heading first and label the dialog: `<dialog aria-labelledby="sheet-title">`.

## 3. Non-modal sheets
Persistent sheets (maps, media players) use `dialog.show()` or a plain region; they don't trap focus, so keep them reachable in tab order.

## 4. Pitfalls
- On-screen keyboard covers inputs in the sheet: `interactive-widget=resizes-content` in the viewport meta (MDN compat data: Chrome on Android 108+ only) or the VirtualKeyboard API (Chromium, secure contexts only), and `scrollIntoView` focused fields.
- Long content: the sheet scrolls internally; keep the action bar sticky inside it.

## Verify
- [ ] Desktop shows a centred modal, mobile a bottom sheet; focus moves in and returns to the trigger; Esc and close button work; content clears the home indicator and keyboard.

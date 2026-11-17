---
id: computing-software.web-development.web-accessibility.content-on-hover-or-focus
name: content-on-hover-or-focus
category: computing-software
field: web-development
product: web-accessibility
tags: [distinguishable, content-on-hover-focus, accessible-tooltips, wcag-1-4-13, popovers]
level: practitioner
status: docs-checked
description: "Building tooltips and hover cards that meet WCAG 1.4.13: dismissible with Escape, hoverable without vanishing, persistent until dismissed, and shown on keyboard focus."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html
  - https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/popover
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Content on hover or focus

**1.4.13 (AA):** when pointer hover or keyboard focus shows extra content (tooltips, hover cards, mega-menus, custom title popups), it must be:
1. **Dismissible** without moving pointer or focus (Escape), unless it conveys an input error or doesn't obscure other content.
2. **Hoverable**: the pointer can move onto the new content without it disappearing (screen magnifier users need this).
3. **Persistent**: stays visible until hover/focus is removed, the user dismisses it, or its information is no longer valid - no timeouts.
Content whose presentation is determined by the user agent and not modified by the author, such as the browser's own `title` tooltip, is exempt.

## 1. Tooltip implementation
```html
<button type="button" aria-describedby="tip-save" class="has-tip">Save</button>
<div role="tooltip" id="tip-save" class="tip" hidden>Saves a draft (Ctrl+S)</div>
```
```js
let hideTimer;
const show = () => { clearTimeout(hideTimer); tip.hidden = false; };
const hide = () => { hideTimer = setTimeout(() => (tip.hidden = true), 150); };  // grace period lets pointer travel
for (const el of [btn, tip]) { el.addEventListener("pointerenter", show); el.addEventListener("pointerleave", hide); }
btn.addEventListener("focus", show); btn.addEventListener("blur", () => (tip.hidden = true));
document.addEventListener("keydown", e => { if (e.key === "Escape") tip.hidden = true; });
```
- No gap between trigger and tooltip (or the grace delay) so it's hoverable.
- Tooltips contain plain text only - no links or buttons. Interactive content belongs in a disclosure/popover opened by click.
- Use `aria-describedby` for supplementary descriptions; an icon-only button's name should be `aria-label`/text, with the tooltip mirroring it.
- `popover="hint"` (documented on MDN) gives hint popovers that can be light dismissed.

## 2. Hover menus
Mega-menus opening on hover must also open on focus/click, close on Escape, and not close when the pointer moves diagonally toward the submenu (for example with a short close delay).

## 3. Touch
Hover doesn't exist; make the info available on tap or visible by default.

## Verify
Keyboard: focus shows tooltip, Escape hides it without moving focus. Mouse: move from trigger onto the tooltip - it stays. Wait: it doesn't time out. Zoom in: the tooltip can be dismissed if it covers content you need.

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text of 1.4.13 (Level AA): dismissible (unless it communicates an input error or does not obscure other content), hoverable, persistent (until hover or focus is removed, the user dismisses it, or the information is no longer valid) and the user-agent exception, which the Understanding page illustrates with the title attribute tooltip. Removed the interestfor claim, the 400% zoom figure and the 30 s figure; the third-party article source is dropped.

Method: documentation only; no commands were run.

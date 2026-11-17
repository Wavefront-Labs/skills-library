---
id: computing-software.web-development.web-accessibility.inert-and-hiding-background-content
name: inert-and-hiding-background-content
category: computing-software
field: web-development
product: web-accessibility
tags: [keyboard-accessibility, inert-attribute, aria-hidden, modal-dialogs, focus-management]
level: practitioner
status: verified
description: "Hiding background content while modals, drawers and menus are open using the inert attribute instead of aria-hidden hacks, and avoiding focusable hidden content."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/inert
  - https://html.spec.whatwg.org/multipage/interaction.html#the-inert-attribute
  - https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# inert and hiding background content

## 1. The problem
When an overlay is open, keyboard and screen-reader users can wander into the page behind it (virtual cursor, Tab), interacting with content they can't see. Off-canvas menus and collapsed panels left focusable cause "invisible focus" (WCAG 2.4.3, 2.4.7, 2.4.11).

## 2. inert (Baseline 2023)
```html
<div id="app" inert>…page…</div>
<div class="drawer" role="dialog" aria-modal="true" aria-labelledby="dt">…</div>
```
```js
function openDrawer() { app.inert = true; drawer.hidden = false; drawer.querySelector("[autofocus], button").focus(); }
function closeDrawer() { app.inert = false; drawer.hidden = true; trigger.focus(); }
```
`inert` removes the subtree from the tab order, blocks pointer events and clicks, removes it from the accessibility tree (run: Chromium's full AX tree dropped the inert button), and blocks find-in-page and text selection (MDN). The overlay must be **outside** the inert subtree (render overlays as siblings of `#app`, e.g. via portal).

## 3. Prefer the platform when possible
- `<dialog>.showModal()` makes everything else inert automatically (run: the background buttons left the AX tree and the Tab order; Tab can still reach browser UI).
- Hidden content: `hidden`, `display: none` or `visibility: hidden` remove it from focus and AT. `opacity: 0`, `transform: translateX(-100%)`, `height: 0; overflow: hidden` **don't** (run: all three buttons stayed in the Tab order) - a closed off-canvas menu that only translates away remains tabbable. Add `visibility: hidden` after the close transition (transition `visibility` with a delay) or `inert` on the closed panel.

## 4. aria-hidden vs inert
- `aria-hidden="true"` hides from AT but **not** from keyboard (run) - focusable children remain tabbable and announced as nothing (axe `aria-hidden-focus`). Old modal scripts set `aria-hidden` on siblings plus a JS focus trap; `inert` replaces both.
- Never put `aria-hidden="true"` on `body` or an ancestor of the open dialog.

## 5. Gotchas
- Polyfill (`wicg-inert`) only for old Safari < 15.5 if your analytics need it.
- Styling: browsers don't dim inert content - add your own backdrop.
- Toasts/live regions inside an inert tree won't be announced; place them outside.

## Verify
Open each overlay: Tab cycles only inside it; screen reader virtual cursor can't reach the background (NVDA browse mode arrows); closed drawers aren't reachable by Tab.

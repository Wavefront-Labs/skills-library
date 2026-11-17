---
id: computing-software.web-development.web-accessibility.keyboard-navigation-and-focus-management
name: keyboard-navigation-and-focus-management
category: computing-software
field: web-development
product: web-accessibility
tags: [keyboard-navigation, focus-management, tabindex, skip-link, focus-trap, focus-visible, tab-order, accessibility, web-development]
level: advanced
status: docs-checked
description: "Keyboard navigation and focus management: tab order pitfalls, skip links, focus traps for modals, and :focus-visible vs removing outlines."
sources:
  - https://www.w3.org/WAI/WCAG21/Understanding/keyboard-accessible.html
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/tabindex
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:focus-visible
  - https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyboard navigation and focus management

**Goal:** everything a mouse can do, a keyboard-only user can also do, in an
order that matches what they see, with the current position always visible.

## 1. `tabindex` values — only three are ever correct
- **`tabindex="0"`**: makes a non-naturally-focusable element (a `div` acting as
  a button) part of the natural tab order, in document order. The only value to
  use when adding focusability to custom elements.
- **`tabindex="-1"`**: removes an element from the tab sequence but allows
  programmatic focus (`el.focus()`) — used for a modal's heading or a target you
  scroll/focus to after an action, not reachable by Tab itself.
- **Any positive value (`tabindex="1"`, `"2"`...)**: overrides document order
  with an explicit numeric sequence. Almost always wrong — it's exceptionally
  easy to create an order that doesn't match visual layout, and mixing numbered
  and `0` elements produces a sequence that confuses everyone including the
  person who wrote it. If visual and DOM order genuinely diverge (a CSS grid
  reorder), fix the DOM order instead of patching it with positive tabindex.

## 2. Skip links — bypass repeated navigation
```html
<a href="#main-content" class="skip-link">Skip to main content</a>
<!-- visually hidden until focused, then visible -->
```
Without one, a keyboard user re-tabs through the entire header/nav on every
single page before reaching content — tedious on page 1, unacceptable on page
50. The link must be one of the very first focusable elements in the DOM, and
must become visible on focus (hiding it entirely with `display:none` makes it
unreachable even by keyboard).

## 3. Focus traps — modals need one, page navigation must not have one
A modal dialog needs focus deliberately contained inside it while open: Tab
from the last focusable element cycles to the first, Shift+Tab from the first
cycles to the last, and Escape closes it and returns focus to the trigger.
Implement with a library (`focus-trap`) or the native `<dialog>` element's
`showModal()`, which makes the rest of the page inert, sets initial focus and
closes on Escape, rather than hand-rolling it. The opposite failure — focus getting stuck somewhere on the
regular page (a sticky dropdown that captures Tab and never releases it) — is a
bug, not a feature; only an explicit modal should trap focus at all.

## 4. `:focus-visible`, not deleting the outline
`* { outline: none; }` is one of the most common accessibility violations in
real codebases — it removes the only visual indicator of keyboard position for
every user, including mouse users who tab by habit. `:focus-visible` (native
CSS, Baseline widely available since March 2022) shows the indicator only when the browser determines
keyboard/non-pointer interaction caused the focus, leaving mouse clicks free of
an outline if that's the look you want:
```css
button:focus-visible { outline: 2px solid #2563eb; outline-offset: 2px; }
button:focus { outline: none; }  /* mouse-triggered focus: no ring, but :focus-visible still fires for keyboard */
```
Never remove focus styling without replacing it with an equally visible
alternative. WCAG 2.4.7 Focus Visible (AA) requires a visible indicator, 1.4.11
Non-text Contrast (AA) asks for 3:1 for visual information that identifies
component states, and 2.4.13 Focus Appearance (AAA) sets size and contrast.

## 5. Managing focus after SPA route changes and dynamic content
On a client-side route change, move focus to the new page's heading (or a
dedicated "page content" landmark with `tabindex="-1"`) and announce the route
change via a live region — without this, a screen reader user's focus stays on
the now-stale link they clicked, with no indication anything happened. After
closing a modal/dismissing a toast, return focus to the element that triggered
it, not to `<body>` (which silently resets keyboard position to the top of the
page).

## Verify
- [ ] No positive `tabindex` values exist; divergent visual/DOM order is fixed at the DOM level.
- [ ] A skip link is present, is one of the first few focusable elements, and becomes visible on focus.
- [ ] Every modal traps focus while open and restores it to the trigger on close; nothing outside a modal does.
- [ ] `:focus-visible` (or equivalent) provides a clearly visible indicator; no blanket `outline: none`.
- [ ] SPA route changes move focus to new content and announce the change; closing an overlay returns focus to its trigger.

## Checked

- Date: 2026-10-26. Documentation: MDN tabindex, dialog and :focus-visible, web-features data, ARIA APG modal dialog pattern, WebAIM keyboard techniques, WCAG 2.2.
- Confirmed: only `0` and `-1` are recommended `tabindex` values and positive values should be avoided; `-1` allows programmatic focus; modal dialogs contain Tab, close on Escape and return focus to the invoker; `showModal()` makes the rest of the page inert; `:focus-visible` is Baseline widely available (2022-03-14); WebAIM warns against `outline: none` and recommends a skip link; 2.4.7 and 1.4.11 are AA, 2.4.13 is AAA.
- Removed: the "similar contrast ratio to body text" rule of thumb.
Method: documentation only; no commands were run.
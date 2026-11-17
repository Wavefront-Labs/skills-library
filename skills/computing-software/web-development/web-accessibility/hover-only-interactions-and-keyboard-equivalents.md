---
id: computing-software.web-development.web-accessibility.hover-only-interactions-and-keyboard-equivalents
name: hover-only-interactions-and-keyboard-equivalents
category: computing-software
field: web-development
product: web-accessibility
tags: [hover-only-interactions, keyboard-accessibility, mega-menus, touch-accessibility, wcag-2-1-1]
level: practitioner
status: docs-checked
description: "Fixing hover-only interactions: menus, tooltips, card actions and previews that need a mouse, with keyboard and touch equivalents via focus-within and disclosure buttons."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html
  - https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html
  - https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hover-only interactions and keyboard equivalents

Anything that appears or works only on `:hover`/`mouseenter` fails keyboard users (2.1.1), and often touch and screen-reader users too.

## 1. Common offenders and fixes
| Pattern | Fix |
|---|---|
| Dropdown nav opens on hover | Disclosure button per top-level item (`aria-expanded`), hover as an extra for mouse |
| Card actions (edit/delete) visible on hover only | Always visible on touch/keyboard: show on `:hover, :focus-within`, and on `@media (hover: none)` show permanently |
| Tooltip with essential info | Show on focus too; better, put the info in visible text or a toggletip button |
| Image zoom / preview on hover | Button to open the preview; or show on focus |
| Hover-to-reveal password/hint | Explicit toggle button |
| Draggable reorder with hover handles | Visible handle buttons plus move up/down actions |

## 2. CSS
```css
.card .actions { opacity: 0; }
.card:hover .actions, .card:focus-within .actions { opacity: 1; }
@media (hover: none) { .card .actions { opacity: 1; } }
```
Use `opacity` (still focusable) rather than `display: none`/`visibility: hidden` - otherwise keyboard users can't Tab into the hidden actions to reveal them.

## 3. Menus
```html
<li><button aria-expanded="false" aria-controls="m-products">Products</button>
  <ul id="m-products" hidden> ... </ul></li>
```
Click/Enter/Space toggles; Esc closes an open menu (needed for 1.4.13, per the APG disclosure navigation example); hover may open after a short delay with a grace period when leaving (pointer intent). Don't make the top-level label both a link and the hover trigger with no separate toggle.

## 4. Content shown on hover or focus (1.4.13)
When additional content does appear: dismissible with Esc without moving the pointer, hoverable (the pointer can move onto it), persistent until dismissed.

## 5. Testing
Unplug the mouse: Tab through every component and confirm each hover feature is reachable. On a touch device, check that first tap doesn't trigger hover-only states that block the link.

## Verify
- [ ] Every hover-revealed control reachable and operable by keyboard and touch; menus operate via buttons; tooltips dismissible with Esc.

## Checked

- Date: 2026-10-26. Documentation: WCAG 2.2 (2.1.1, 1.4.13), ARIA APG disclosure navigation example.
- Confirmed: 1.4.13 Content on Hover or Focus is AA and requires dismissible, hoverable and persistent content; APG disclosure navigation uses buttons with `aria-expanded` and closes on Esc.
- Removed: the claim that Esc returns focus (not stated in the APG example).
Method: documentation only; no commands were run.
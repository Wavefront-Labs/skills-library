---
id: computing-software.web-development.web-accessibility.icon-buttons-and-accessible-svg
name: icon-buttons-and-accessible-svg
category: computing-software
field: web-development
product: web-accessibility
tags: [text-alternatives, icon-buttons, accessible-svg, accessible-name, wcag-4-1-2]
level: practitioner
status: verified
description: "Giving icon-only buttons and links accessible names: visually hidden text vs aria-label, hiding the SVG, tooltips, toggle states, and voice-control label-in-name."
sources:
  - https://www.sarasoueidan.com/blog/accessible-icon-buttons/
  - https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html
  - https://www.w3.org/TR/accname-1.2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Icon buttons and accessible SVG names

## 1. Patterns (pick one)
```html
<!-- A: visually hidden text (translates with page, works everywhere) -->
<button type="button"><svg aria-hidden="true" focusable="false">…</svg><span class="visually-hidden">Close dialog</span></button>

<!-- B: aria-label -->
<button type="button" aria-label="Close dialog"><svg aria-hidden="true" focusable="false">…</svg></button>

<!-- C: labelled SVG (when the svg itself carries the name) -->
<a href="/cart"><svg role="img" aria-labelledby="cart-t"><title id="cart-t">Cart</title>…</svg></a>
```
All three patterns gave the expected names in Chromium's AX tree ("Close dialog" twice, link "Cart"; run). B is simplest; A keeps the name as page text. Always hide decorative SVG inside a named control so it isn't read twice.

## 2. Wording
- Name the action/destination: "Search", "Close", "Edit address", not "X", "magnifying glass", "pencil".
- Repeated icons per row need distinct names: "Delete invoice 1043" (or `aria-describedby` to the row title).
- Toggle buttons keep a stable name and expose state: `aria-pressed="true"` (e.g. "Mute" pressed), or change the label ("Show password"/"Hide password") - not both.

## 3. Tooltips
Icon-only buttons benefit sighted users from a visible tooltip on hover **and focus**, dismissible with Escape (WCAG 1.4.13). Don't rely on the `title` attribute (not shown on focus/touch, inconsistently announced).

## 4. Voice control
Users say what they see. If a visible tooltip/text says "Settings", the accessible name must contain "Settings" (WCAG 2.5.3 label in name).

## 5. Size
Icon buttons need a target of at least 24x24 CSS px (2.5.8 AA), 44x44 recommended - pad the button, not the icon.

## Verify
axe `button-name`, `link-name`, `svg-img-alt`; DevTools Accessibility pane shows the computed name; screen reader announces "Close dialog, button".

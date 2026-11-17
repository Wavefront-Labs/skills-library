---
id: computing-software.web-development.web-accessibility.apg-menu-button-and-navigation-menus
name: apg-menu-button-and-navigation-menus
category: computing-software
field: web-development
product: web-accessibility
tags: [aria-patterns, menu-button-pattern, menu, disclosure-navigation, wai-aria-apg]
level: practitioner
status: docs-checked
description: "Choosing and building menus correctly: APG menu button with role=menu for app actions vs disclosure navigation for site links, keyboard behaviour, focus and dismissal."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/
  - https://www.w3.org/WAI/ARIA/apg/patterns/menubar/
  - https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Menu button and navigation menus

## 1. Pick the right pattern
- **Site navigation** (links to pages, including dropdown submenus): **disclosure** - buttons with `aria-expanded` revealing lists of links. Do not use `role="menu"`.
- **Application actions** (like a desktop app's "More actions": Edit, Duplicate, Delete): **menu button** with `role="menu"` / `menuitem`.
`role="menu"` expects the arrow-key model of a desktop menu; for site navigation the APG offers the disclosure navigation example (buttons with `aria-expanded` revealing link lists), which is the approach this skill recommends. APG also contains a Navigation Menu Button example that uses `role="menu"` with links, so it is a design choice, not a rule.

## 2. Menu button (APG)
```html
<button type="button" id="actions-btn" aria-haspopup="menu" aria-expanded="false" aria-controls="actions-menu">Actions</button>
<ul role="menu" id="actions-menu" aria-labelledby="actions-btn" hidden>
  <li role="menuitem" tabindex="-1">Duplicate</li>
  <li role="menuitem" tabindex="-1">Rename</li>
  <li role="separator"></li>
  <li role="menuitem" tabindex="-1" aria-disabled="true">Delete</li>
</ul>
```
Keyboard:
- Enter/Space on the button: open the menu and focus the first item. Optional: Down Arrow opens and focuses the first item; Up Arrow opens and focuses the last.
- Down/Up Arrow move to the next/previous item (wrapping is optional); Home/End go to first/last when wrapping is not supported; a printable character (optional) moves to the next item starting with it.
- Enter activates, then menu closes and focus returns to the button.
- Escape closes the menu and returns focus to the button. Tab and Shift+Tab do not move focus among menu items.
- `menuitemcheckbox` / `menuitemradio` with `aria-checked` for toggles.
Pointer: close on outside click.

## 3. Disclosure navigation
```html
<nav aria-label="Main"><ul>
  <li><button type="button" aria-expanded="false" aria-controls="sub-products">Products</button>
      <ul id="sub-products" hidden><li><a href="/laptops">Laptops</a></li>…</ul></li>
  <li><a href="/pricing" aria-current="page">Pricing</a></li>
</ul></nav>
```
Tab moves through links naturally; Escape closes an open submenu and sets focus on the button that controls it; Down/Right Arrow between buttons are optional in the APG example. Don't open on hover only.

## 4. Pitfalls
- `aria-haspopup="menu"` (or `true`, which means menu) on disclosure-style site nav buttons: the APG disclosure navigation example uses only `aria-expanded`.
- Not closing other open menus.

## Verify
Screen reader announces "Actions, menu button, collapsed"; arrow keys work inside; Escape returns focus; site nav announces "button, expanded" and links as links.

## Checked

2026-10-26, against WCAG 2.2 / APG as of 2026-10-26 (w3c repos). Confirmed against the APG menu button, menu and menubar, and disclosure navigation pages: Enter/Space/Down/Up on the button, aria-haspopup menu or true, aria-expanded, optional aria-controls, Escape returning focus, Tab not moving among items, type-ahead optional, and the disclosure navigation Escape behaviour. Removed the unconfirmed popover and middle-click claims and corrected the haspopup advice.

Method: documentation only; no commands were run.

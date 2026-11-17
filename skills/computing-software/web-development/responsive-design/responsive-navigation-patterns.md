---
id: computing-software.web-development.responsive-design.responsive-navigation-patterns
name: responsive-navigation-patterns
category: computing-software
field: web-development
product: responsive-design
tags: [responsive-components, responsive-navigation, disclosure-menu, priority-plus, accessibility]
level: practitioner
status: verified
description: "Building responsive site navigation: disclosure (hamburger) menus done accessibly, priority+ overflow, bottom tabs, and avoiding hover-only and focus-trap mistakes."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/
  - https://css-tricks.com/the-priority-navigation-pattern/
  - https://www.nngroup.com/articles/hamburger-menus/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responsive navigation patterns

## 1. Pick by item count
- <= 5 items: show them all; wrap or shrink labels. Bottom tab bar for app-like mobile UIs.
- 5-10: priority+ (show what fits, overflow into "More").
- Large sites: disclosure (hamburger) menu on mobile, mega menu on desktop. NN/g: hidden navigation is less discoverable than visible navigation (their testing: "Discoverability is cut almost in half") - keep key actions (search, cart) visible.

## 2. Disclosure menu (not an ARIA menu)
```html
<nav aria-label="Main">
  <button type="button" aria-expanded="false" aria-controls="main-menu" class="menu-toggle">Menu</button>
  <ul id="main-menu" hidden>…links…</ul>
</nav>
```
```js
toggle.addEventListener("click", () => {
  const open = toggle.getAttribute("aria-expanded") === "true";
  toggle.setAttribute("aria-expanded", String(!open));
  menu.hidden = open;
});
// run in Chromium 156: Tab focused the toggle, Enter set aria-expanded=true and unhid the list, Escape hid it and refocused the toggle
document.addEventListener("keydown", e => { if (e.key === "Escape" && !menu.hidden) { menu.hidden = true; toggle.setAttribute("aria-expanded", "false"); toggle.focus(); } });
```
- Use links in a list, not `role="menu"` (menus imply app-style arrow-key behaviour users don't expect for site nav).
- Visible label "Menu" next to the icon improves recognition; icon-only needs an accessible name.
- Desktop: show the list with CSS (`@media (width >= 60rem) { #main-menu { display: flex } .menu-toggle { display: none } }`); the author `display: flex` overrides the `hidden` attribute, so the list shows at 1200px even though `hidden` is still set (run in Chromium 156), but `hidden` then misreports state if the viewport shrinks, so reset it with `matchMedia` in JS.
- Full-screen overlay menus behave like modals - trap focus and make background inert; plain dropdown panels should not trap.

## 3. Priority+
Measure available width (ResizeObserver), move overflowing items into a "More" disclosure. Keep DOM order identical in both places for screen readers.

## 4. Submenus
Use disclosure buttons for submenus (click/Enter to open). Hover-only flyouts fail touch and keyboard users and WCAG 1.4.13 if they can't be dismissed.

## 5. Current page
`aria-current="page"` on the active link, with a visible style.

## Verify
Keyboard: Tab to toggle, Enter opens, Tab through links, Escape closes and refocuses; screen reader announces "Menu, button, collapsed/expanded"; works at 320px and with 200% text.

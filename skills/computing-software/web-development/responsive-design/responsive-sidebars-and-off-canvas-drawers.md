---
id: computing-software.web-development.responsive-design.responsive-sidebars-and-off-canvas-drawers
name: responsive-sidebars-and-off-canvas-drawers
category: computing-software
field: web-development
product: responsive-design
tags: [off-canvas-drawer, responsive-sidebar, navigation-drawer, inert, responsive-design]
level: practitioner
status: verified
description: "Responsive sidebar that becomes an off-canvas drawer on small screens: layout with grid, toggling with dialog or popover, inert background, focus return and no-JS fallback."
sources:
  - https://web.dev/articles/building/a-sidenav-component
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/inert
  - https://developer.mozilla.org/en-US/docs/Web/API/Popover_API
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responsive sidebars and off-canvas drawers

## 1. Layout
```css
.layout { display: grid; grid-template-columns: 16rem 1fr; min-block-size: 100dvh; }
.sidebar { position: sticky; top: 0; block-size: 100dvh; overflow-y: auto; }
@media (width < 60rem) {
  .layout { grid-template-columns: 1fr; }
  .sidebar { position: fixed; inset-block: 0; inset-inline-start: 0; inline-size: min(20rem, 85vw);
             translate: -100% 0; transition: translate .25s; z-index: 10; }
  .sidebar[data-open] { translate: 0 0; }
}
@media (prefers-reduced-motion: reduce) { .sidebar { transition: none; } }
```
Use logical properties so the drawer slides from the right in RTL, and flip the translate with `:dir(rtl)`: run in Chromium 156 at 400px, with `inset-inline-start: 0` and `translate: -100% 0` in an RTL page the closed drawer sat at x -240 to 80, leaving an 80px sliver visible, while `translate: 100% 0` for RTL put it at x 400 to 720 (off-screen). Add `@media (width < 60rem) { :dir(rtl) .sidebar { translate: 100% 0 } :dir(rtl) .sidebar[data-open] { translate: 0 0 } }`.

## 2. Toggling on mobile
Simplest robust option: render the mobile drawer as a modal `<dialog>` (focus trap, Esc, inert page included), and keep the desktop sidebar as a plain `<nav>`.
```html
<button aria-controls="drawer" aria-expanded="false" id="menu-btn">Menu</button>
<dialog id="drawer" aria-label="Site navigation" class="drawer"> <nav>...</nav> <button>Close</button> </dialog>
```
Alternative: `popover` attribute with `popovertarget` (light dismiss, top layer, no JS; Baseline newly available 2025-01-27) - but popovers are non-modal, so the page behind stays focusable (run: Tab moved into the popover then on to the link behind it, Esc closed it); acceptable for navigation, not for forms.

If you hand-roll it:
- Set `inert` on `<main>` and other siblings while open; remove on close.
- Move focus to the first link or the drawer heading on open; return it to the toggle on close; update `aria-expanded`.
- Close on Esc, backdrop click, and after navigating.

## 3. Desktop collapse
Collapsible desktop rail (icons only): animate `grid-template-columns` from `16rem 1fr` to `4rem 1fr` (interpolates in modern browsers; run: 101.9px 682.1px mid-transition and 64px 720px at the end in Chromium 156); keep accessible names on icon links via visually hidden text, and show tooltips on hover/focus.

## 4. No-JS fallback
Without JS, show the navigation inline above content on mobile (or at the bottom with a skip link), never hidden off-screen with no way to open it.

## Verify
- [ ] At narrow widths drawer opens, traps focus (or page is inert), closes on Esc and returns focus; at wide widths sidebar is sticky and scrolls independently; RTL slides from the right.

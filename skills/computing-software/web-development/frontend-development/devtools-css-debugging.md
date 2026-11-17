---
id: computing-software.web-development.frontend-development.devtools-css-debugging
name: devtools-css-debugging
category: computing-software
field: web-development
product: frontend-development
tags: [css-debugging, grid-overlay, flexbox-overlay, styles-pane, rendering-emulation, chrome-devtools]
level: practitioner
status: docs-checked
description: "Debugging CSS in DevTools: overridden vs invalid declarations, Computed tracing, grid/flex overlays, forced states, inactive-CSS hints, Rendering emulation and overflow hunting."
sources:
  - https://developer.chrome.com/docs/devtools/css/reference
  - https://developer.chrome.com/docs/devtools/css/grid
  - https://firefox-source-docs.mozilla.org/devtools-user/page_inspector/how_to/examine_grid_layouts/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DevTools CSS debugging

## 1. Read the Styles pane
- Struck-through declaration: valid but overridden (check the winning rule above it).
- Warning triangle: invalid value or unknown property (typo, unsupported syntax).
- Inactive CSS: a declaration that is valid but has no effect on that element; DevTools hints at the reason (e.g. `width` on an inline element, `align-items` on a non-flex parent).
- Computed tab: shows only the CSS actually applied; the Show All checkbox includes inherited and default properties, and the filter box searches properties or values.

## 2. Layout overlays
- Use the Chrome grid debugging page and Firefox's grid layout page (both cited in sources) to turn on grid overlays (line numbers, area names, track sizes) for the element you are debugging.

## 3. Hunting overflow and stacking issues
```js
// who is wider than the viewport?
[...document.querySelectorAll("*")].filter(el => el.getBoundingClientRect().right > document.documentElement.clientWidth);
```
```css
* { outline: 1px solid rgb(255 0 0 / .3); }   /* temporary: see every box */
```
When `z-index` misbehaves, look for the stacking context that contains the element.

## 4. Rendering tab emulation
The Rendering tab in Chrome DevTools can emulate CSS media features (such as color scheme and reduced motion) and highlight paint and layout-shift activity; see the DevTools docs for the current list.

## 5. Keep your edits
DevTools edits are lost on reload unless you copy them back to source; keep a note of each change as you go.

## Verify
- [ ] For a broken layout you can name the winning rule (Computed), whether it is inactive (Styles hint) and the grid track it lands in (overlay).

## Checked
2026-10-28. Confirmed on Chrome DevTools CSS reference: Styles shows overridden declarations; invalid, overridden and inactive CSS view; Computed tab, Show All checkbox and filter box. Removed: `:hov` and `.cls` behaviours, badge and Layout pane details, Firefox claims, Layers/3D View, the Rendering list, Changes tab shortcut and Workspaces (not on fetched pages).
Method: documentation only; no commands were run.

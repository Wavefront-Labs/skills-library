---
id: computing-software.web-development.frontend-development.flexbox-alignment
name: flexbox-alignment
category: computing-software
field: web-development
product: frontend-development
tags: [flexbox, flex-alignment, justify-content, align-items, margin-auto, css]
level: practitioner
status: docs-checked
description: "Aligning flex items correctly: justify-content vs align-items vs align-content, align-self overrides, margin auto tricks, safe alignment and baseline alignment."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Aligning_items
  - https://www.w3.org/TR/css-align-3/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/justify-content
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flexbox alignment

## 1. Axes
`justify-*` = main axis (row: horizontal); `align-*` = cross axis. Switching `flex-direction: column` swaps them visually.

## 2. Properties
| Property | On | Aligns |
|---|---|---|
| `justify-content` | container | distribution of items along main axis: `flex-start`, `center`, `space-between`, `space-around`, `space-evenly`, `flex-end` |
| `align-items` | container | each item on the cross axis within its line: `stretch` (default), `flex-start`, `center`, `baseline`, `last baseline` |
| `align-self` | item | override for one item |
| `align-content` | container | distribution of **lines** - only matters with `flex-wrap: wrap` and extra cross space |
`justify-items`/`justify-self` do nothing in flexbox.

## 3. margin: auto
Auto margins absorb free space before `justify-content` applies:
```css
.nav { display: flex; gap: 1rem; }
.nav .account { margin-inline-start: auto; }    /* push last group to the end */
.center-me { margin: auto; }                    /* perfect centring in both axes */
```

## 4. Recipes
- Centre anything: `display: flex; align-items: center; justify-content: center;` (or grid `place-items: center`).
- Icon + text baseline: `align-items: baseline` keeps different font sizes aligned on text baseline; for icons use `center`.
- Equal-height cards: default `stretch` does it; set `align-items: start` when you don't want stretching (e.g. images).
- Button at the bottom of each card: card `display: flex; flex-direction: column`, button `margin-block-start: auto`.

## 5. Safe alignment
`justify-content: center` with overflowing content pushes items off the start edge where they can't be scrolled to. Use `justify-content: safe center` (Chrome 115, Firefox 63, Safari 17.6; Chrome before 115 recognises it but ignores it) or margin auto, which behaves safely.

## Verify
Resize narrow to confirm no unreachable overflow.

## Checked
2026-10-26. MDN aligning-items guide and justify-content page, plus browser-compat-data (main, 2026-10-26): confirmed justify-items/justify-self do not apply on the flex main axis (auto margins are used instead), align-items accepts baseline, first baseline and last baseline, and the safe keyword support versions. Removed the unconfirmed DevTools editor claim.
Method: documentation only; no commands were run.

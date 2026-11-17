---
id: computing-software.web-development.frontend-development.grid-repeat-auto-fit-minmax
name: grid-repeat-auto-fit-minmax
category: computing-software
field: web-development
product: frontend-development
tags: [css-grid, auto-fit-minmax, auto-fill, responsive-grid, css]
level: practitioner
status: docs-checked
description: "Building responsive card grids with repeat(auto-fit or auto-fill, minmax()) without media queries: the difference between auto-fit and auto-fill and overflow-safe minimums."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/repeat
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/minmax
  - https://www.w3.org/TR/css-grid-2/#auto-repeat
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# repeat(auto-fit / auto-fill, minmax())

## 1. The one-liner
```css
.cards { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fill, minmax(min(16rem, 100%), 1fr)); }
```
- Creates as many columns as fit at >= 16rem, then stretches them with `1fr`.
- `min(16rem, 100%)` prevents overflow when the container is narrower than 16rem (otherwise a 16rem column overflows on small phones).

## 2. auto-fill vs auto-fit
Only differs when there are fewer items than columns that fit:
- `auto-fill` keeps the empty tracks - 2 items in a wide container stay card-sized, aligned with a full grid.
- `auto-fit` collapses empty tracks to 0 - 2 items stretch to fill the whole row.
Card galleries usually want `auto-fill` (consistent card width); a row of 2-4 feature boxes that should fill the width wants `auto-fit`.

## 3. Capping column count
```css
/* at most 4 columns */
grid-template-columns: repeat(auto-fill, minmax(max(16rem, (100% - 3 * 1rem) / 4), 1fr));
```

## 4. Limits
- Intrinsic: column count depends on container width, not viewport - works inside sidebars. For components, container queries add finer control.
- In an auto-repeat, each track size must be a `<length-percentage>` or a `minmax()` where at least one of min and max is a `<length-percentage>`; bare `auto` and `minmax(auto, 1fr)` are invalid.
- Rows: set `grid-auto-rows: 1fr` for equal-height rows, or let content decide.

## Verify
Resize from 320px to 1600px: column count changes smoothly, nothing overflows; test with 1, 2 and 20 items for auto-fill vs auto-fit behaviour.

## Checked

Checked 2026-10-26 against current documentation. MDN `repeat()` (auto-fill/auto-fit semantics, collapse of empty tracks, `<fixed-size>` rules for auto-repeat) and `minmax()`. Fixed: in an auto-repeat at least one of min or max must be a length-percentage (the skill said the minimum must be).

Method: documentation only; no commands were run.

---
id: computing-software.web-development.frontend-development.align-content-and-place-content
name: align-content-and-place-content
category: computing-software
field: web-development
product: frontend-development
tags: [align-content, place-content, flexbox, css-grid, box-alignment]
level: practitioner
status: docs-checked
description: "Aligning multi-line flex containers and grid tracks with align-content, justify-content and place-content: when they apply, free-space distribution, and align-content on blocks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/align-content
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/place-content
  - https://www.w3.org/TR/css-align-3/
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# align-content and place-content

`*-content` properties distribute free space **between lines or tracks**; `*-items`/`*-self` align **items inside their line or cell**. Most confusion comes from mixing the two.

## 1. Flexbox
```css
.tags { display: flex; flex-wrap: wrap; height: 20rem; align-content: flex-start; gap: .5rem; }
```
- `align-content` only does anything when `flex-wrap: wrap` produces multiple lines **and** the container has spare cross-axis space. With one line (nowrap) it has no effect - use `align-items`.
- Default `normal` behaves as `stretch`: lines grow to fill the height, which is why wrapped rows look spaced out in a tall container. `align-content: flex-start` packs them.
- Values: `flex-start | center | flex-end | space-between | space-around | space-evenly | stretch`.

## 2. Grid
```css
.board { display: grid; grid-template-columns: repeat(3, 8rem); height: 100vh;
         place-content: center; }   /* align-content + justify-content: centres the whole track block */
```
Applies when the tracks are smaller than the container (fixed-size tracks, no `fr`). With `fr` units tracks absorb all space, so `*-content` has nothing to distribute.

## 3. Shorthand
`place-content: <align-content> <justify-content>`; one value sets both. Similarly `place-items` and `place-self`.

## 4. Block containers
`align-content: center` now works on plain block containers (Baseline 2024): vertical centring without flex/grid.
```css
.hero { min-height: 60vh; align-content: center; }
```

## 5. Safe alignment
`align-content: safe center` falls back to start when content overflows, preventing content pushed off the top where it can't be scrolled to.

## Verify
- [ ] Wrapped flex lines pack as designed in tall containers; centred grids don't clip on small viewports (use `safe`); no `align-content` on single-line flex expecting an effect.

## Checked

Checked 2026-10-26 against current documentation. MDN `align-content` (no effect on single-line flex containers, `safe`/`unsafe` keywords, values) and browser-compat-data (block containers: Chrome 123, Firefox 125, Safari 17.4; `safe`: Chrome 115, Firefox 63, Safari 17.6). No wrong claims found.

Method: documentation only; no commands were run.

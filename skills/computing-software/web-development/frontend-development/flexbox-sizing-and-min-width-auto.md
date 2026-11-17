---
id: computing-software.web-development.frontend-development.flexbox-sizing-and-min-width-auto
name: flexbox-sizing-and-min-width-auto
category: computing-software
field: web-development
product: frontend-development
tags: [flexbox, flex-basis, min-width-zero, flex-grow, flex-shrink, css, flex-min-width, flex-text-truncation]
level: practitioner
status: docs-checked
description: "Understanding flex-grow, flex-shrink and flex-basis, the flex shorthand values, and fixing the min-width auto overflow bug with min-width 0 and text truncation."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/flex
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/flex-basis
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/min-width
  - https://www.w3.org/TR/css-flexbox-1/#min-size-auto
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Flex sizing and the min-width: auto overflow bug

## 1. The algorithm in one paragraph
Each item starts at its `flex-basis` (or its content/`width` if basis is `auto`). Leftover space is distributed in proportion to `flex-grow`; overflow is removed in proportion to `flex-shrink x basis`. Items never shrink below their **automatic minimum size** (`min-width: auto` = min-content width for flex items).

## 2. Shorthands
| `flex:` | Means | Use |
|---|---|---|
| `initial` (default) | `0 1 auto` | size to content, may shrink |
| `auto` | `1 1 auto` | grow from content size - unequal widths |
| `1` | `1 1 0%` | equal columns regardless of content |
| `none` | `0 0 auto` | rigid (icons, avatars) |
| `0 0 240px` | fixed 240px sidebar | |

## 3. The overflow bug
A flex child containing a long word, URL, `<pre>`, table or a nested flex row with `white-space: nowrap` refuses to shrink and blows out the layout, because its min-content width is huge.
```css
.main { flex: 1; min-width: 0; }           /* allow shrinking below content size (column: min-height: 0) */
.title { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
```
A flex or grid item that is a scroll container (`overflow: hidden`, `auto` or `scroll`, but not `clip`) has an automatic minimum size of 0. The same applies to grid items (`minmax(0, 1fr)` instead of `1fr`).
Column direction: scroll areas inside `flex-direction: column` need `min-height: 0` on the flex child to scroll instead of growing.

## 4. Other gotchas
- `flex-basis` beats `width` (except `auto`); `max-width`/`min-width` still clamp.

## Verify
Paste a 200-character unbroken URL into the content - the layout must not overflow horizontally; DevTools flex overlay shows item sizes and shrink amounts.

## Checked

Checked 2026-10-26 against current documentation. MDN `flex` shorthand values (`1` = `1 1 0%`, `auto`, `none`, `initial`), `flex-basis` precedence over `width`, `min-width: auto` for flex and grid items (automatic minimum 0 for scroll containers), and the flexbox spec shrink algorithm (scaled flex shrink factor). Fixed: `overflow: clip` does not create a scroll container, so it does not reset the minimum. Removed unconfirmed image and percent-basis claims.

Method: documentation only; no commands were run.

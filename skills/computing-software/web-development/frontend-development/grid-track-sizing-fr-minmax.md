---
id: computing-software.web-development.frontend-development.grid-track-sizing-fr-minmax
name: grid-track-sizing-fr-minmax
category: computing-software
field: web-development
product: frontend-development
tags: [grid-track-sizing, minmax-function, fr-unit, fit-content, grid-blowout, css-grid]
level: practitioner
status: docs-checked
description: "How CSS Grid sizes tracks: fr and its auto minimum, minmax(0, 1fr) to stop blowouts, fit-content(), min/max-content, auto tracks and percentage-plus-gap overflow."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/minmax
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/grid-template-columns
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/fit-content
  - https://www.w3.org/TR/css-grid-1/#algo-track-sizing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grid track sizing: fr, minmax and friends

## 1. fr is not "equal width"
`1fr` means `minmax(auto, 1fr)`: the track never shrinks below its content's min-content size. A long URL, `<pre>`, wide table or image makes that column wider than its share and the grid overflows ("grid blowout").
```css
.layout { grid-template-columns: minmax(0, 1fr) 300px; }   /* main column can shrink */
.cards  { grid-template-columns: repeat(3, minmax(0, 1fr)); } /* truly equal */
```
Also give the overflowing child `min-width: 0` / `overflow-wrap: anywhere` if it is itself a flex/grid container.

## 2. Track functions
| Value | Behaviour |
|---|---|
| `200px`, `20rem` | fixed |
| `auto` | content-sized; stretches to fill leftover space when `justify-content: normal` |
| `min-content` / `max-content` | narrowest without overflow / widest without wrapping |
| `fit-content(300px)` | like `auto`, capped at 300px (sidebar that shrinks to content) |
| `minmax(150px, 1fr)` | at least 150px, then share leftovers |
| `Nfr` | share of space left after non-fr tracks and gaps |

## 3. Rows
```css
.feed { grid-auto-rows: minmax(120px, auto); }   /* minimum height, grows with content */
.app  { grid-template-rows: auto 1fr auto; min-block-size: 100dvh; }   /* header / content / footer */
```

## 4. Percentages and gaps
`grid-template-columns: 50% 50%; gap: 1rem` overflows by 1rem; percentages ignore gaps. Use `1fr 1fr`.

## 5. Debug
Use the browser DevTools grid overlay to inspect tracks.

## Verify
- [ ] Inserting a 200-character unbroken string into a grid cell does not cause horizontal page scroll.

## Checked

Checked 2026-10-26 against current documentation. MDN `grid-template-columns` (a bare `fr` implies `minmax(auto, <flex>)`; only `auto` tracks are stretched by `justify-content`), `minmax()` (`fr` only valid as max; max below min is ignored) and `fit-content()`. Removed unconfirmed DevTools details.

Method: documentation only; no commands were run.

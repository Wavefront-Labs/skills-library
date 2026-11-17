---
id: computing-software.web-development.frontend-development.css-anchor-positioning
name: css-anchor-positioning
category: computing-software
field: web-development
product: frontend-development
tags: [box-model, anchor-positioning, popover-api, tooltips, css]
level: practitioner
status: docs-checked
description: "Positioning tooltips, menus and popovers relative to an anchor with CSS anchor positioning: anchor-name, position-area, anchor(), fallbacks with position-try, and support."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Anchor_positioning
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Anchor_positioning/Using
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position-area
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/anchor-name
  - https://www.w3.org/TR/css-anchor-position-1/
  - https://github.com/oddbird/css-anchor-positioning
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSS anchor positioning

Replaces JS libraries (Popper/Floating UI) for tethering an element to another, including flipping when out of space.

## 1. Basic tether
```html
<button popovertarget="menu" class="trigger">Options</button>
<div id="menu" popover class="menu">…</div>
```
```css
.trigger { anchor-name: --options; }
.menu {
  position: fixed;                 /* popovers are in the top layer; fixed/absolute both work */
  position-anchor: --options;
  position-area: block-end span-inline-end;   /* below, aligned to start, may extend toward end */
  margin-block-start: 4px;
  position-try-fallbacks: flip-block, flip-inline;   /* flip above / to the other side if clipped */
}
```
- `position-area` places in a 3x3 grid around the anchor (`top center`, `bottom span-right`, ...).
- `anchor()` for precise edges: `top: anchor(bottom); left: anchor(center); translate: -50% 0;`.
- `anchor-size(width)` to match the trigger width: `min-inline-size: anchor-size(inline);`.
- Implicit anchor: the invoker of a popover (via `popovertarget`) is its implicit anchor, so `position-anchor` can be omitted.

## 2. Custom fallbacks
```css
@position-try --above { position-area: block-start; margin: 0 0 4px; }
.menu { position-try-fallbacks: --above, flip-inline; position-try-order: most-height; }
```

## 3. Support
Per browser-compat-data: `anchor-name` and `@position-try` from Chrome 125, `position-try-fallbacks` from Chrome 128, `position-area` from Chrome 129; Firefox 147 and Safari 26 for `anchor-name` and `position-area`. Feature-detect `@supports (anchor-name: --a)` and fall back to Floating UI, or to a simple static placement. Polyfill: `@oddbird/css-anchor-positioning`.

## 4. Pitfalls
- The anchor must be a visible DOM node: if it is `display: none`, the positioned element is placed relative to its nearest positioned ancestor instead.
- Many anchors with the same name: the last one in DOM order wins - scope with `anchor-scope` or unique names per instance.
- Tooltips still need accessible wiring (`aria-describedby`, hover+focus, Escape) - CSS only positions.

## Verify
Scroll and resize so the trigger nears viewport edges - the menu flips instead of clipping; test in a non-supporting browser that the fallback still works.

## Checked

Checked 2026-10-26 against current documentation. MDN (mdn/content main, 2026-10-26) and browser-compat-data: implicit anchor for popover invokers, last same-named anchor wins, `position-area` tile syntax, `position-try-order` keywords, `anchor-scope`, and per-property support versions (Chrome 125/128/129, Firefox 147, Safari 26). The polyfill package name was confirmed from its repository.

Method: documentation only; no commands were run.

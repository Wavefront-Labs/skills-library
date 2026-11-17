---
id: computing-software.web-development.frontend-development.web-animations-api
name: web-animations-api
category: computing-software
field: web-development
product: frontend-development
tags: [canvas-api, element-animate, waapi, animation, javascript, prefers-reduced-motion]
level: practitioner
status: docs-checked
description: "Animating with element.animate(): keyframes and timing, controlling playback, awaiting finished, committing styles, scroll-driven timelines, and reduced-motion handling."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API/Using_the_Web_Animations_API
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/animate
  - https://developer.mozilla.org/en-US/docs/Web/API/Animation/commitStyles
  - https://developer.mozilla.org/en-US/docs/Web/API/ScrollTimeline
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web Animations API (`element.animate`)

## 1. Basic
```js
const anim = el.animate(
  [{ opacity: 0, transform: "translateY(8px)" }, { opacity: 1, transform: "none" }],
  { duration: 200, easing: "cubic-bezier(.2,0,0,1)", fill: "both", delay: 0 }
);
await anim.finished;                     // promise; rejects with AbortError if cancelled
```
Keyframe shorthand: `{ opacity: [0, 1], transform: ["scale(.9)", "none"] }`. Use `offset` for non-uniform stops and `composite: "add"` to stack with existing transforms.

## 2. Control
`anim.pause()`, `play()`, `reverse()`, `finish()`, `cancel()`, `anim.playbackRate = 2`, `anim.currentTime = 100` (scrub). `el.getAnimations()` lists running ones, including CSS animations/transitions - cancel all before starting a new state.

## 3. Keeping the end state
`fill: "forwards"` keeps the final frame, but indefinitely filling animations are discouraged (MDN, Web Animations spec). Better:
```js
anim.onfinish = () => { anim.commitStyles(); anim.cancel(); };   // write final values inline, drop the animation
```
Or set the target style yourself and animate from the old value ("FLIP").

## 4. FLIP for layout changes
```js
const first = el.getBoundingClientRect();
moveInDom(el);                             // apply the change
const last = el.getBoundingClientRect();
el.animate([{ transform: `translate(${first.left-last.left}px, ${first.top-last.top}px)` }, { transform: "none" }], { duration: 250, easing: "ease-out" });
```
(View Transitions do this for whole-page/state changes.)

## 5. Scroll-driven
```js
el.animate({ transform: ["scaleX(0)", "scaleX(1)"] }, { timeline: new ScrollTimeline({ source: document.documentElement }), fill: "both" });
```
`ScrollTimeline` shipped in Chrome 115, Firefox 159 and Safari 26 (browser-compat-data); feature-detect `"ScrollTimeline" in window`. The CSS `scroll()` notation is the declarative counterpart.

## 6. Rules
- Respect `matchMedia("(prefers-reduced-motion: reduce)")` - skip or shorten to an opacity fade.

## Verify
DevTools > Animations panel to scrub; Performance panel shows no layout per frame for the animation.

## Checked

Checked 2026-10-26 against mdn/content (main) Element.animate, Animation.commitStyles and Using the Web Animations API pages, the Web Animations and Scroll-driven Animations drafts (w3c/csswg-drafts) and mdn/browser-compat-data.

- Confirmed: `finished` rejects with an `AbortError` on cancel; `commitStyles()` (Chrome 84, Firefox 75, Safari 13.1) with `cancel()` is the documented alternative to an indefinite `fill`, which the spec discourages; `getAnimations()` also covers CSS animations (CSSAnimation in the spec); `ScrollTimeline` has a `source` and support versions as written; `Element.animate` accepts `timeline`, `rangeStart` and `rangeEnd`.
- Removed: the compositor/layout rule of thumb and the background-tab throttling note, which the pages checked do not state.

Method: documentation only; no commands were run.

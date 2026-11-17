---
id: computing-software.web-development.responsive-design.virtual-keyboard-and-visual-viewport
name: virtual-keyboard-and-visual-viewport
category: computing-software
field: web-development
product: responsive-design
tags: [virtual-keyboard-api, interactive-widget, visualviewport, on-screen-keyboard, mobile-forms, responsive-design]
level: advanced
status: gated
description: "Keeping UI usable when on-screen keyboards open: layout vs visual viewport, interactive-widget viewport setting, VisualViewport and VirtualKeyboard APIs, and fixed footers."
sources:
  - https://developer.chrome.com/blog/viewport-resize-behavior
  - https://developer.mozilla.org/en-US/docs/Web/API/VisualViewport
  - https://developer.mozilla.org/en-US/docs/Web/API/VirtualKeyboard_API
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual keyboard and the visual viewport

## 1. What happens when the keyboard opens
- **iOS Safari** (not run here (gated: unconfirmed, source is paywalled or blocked)): only the *visual* viewport shrinks; the layout viewport (and `100vh`/`100dvh`, `position: fixed; bottom: 0`) stays the same, so fixed footers and chat inputs end up behind the keyboard or float oddly while scrolling.
- **Android Chrome (108+)**: by default also resizes only the visual viewport (`resizes-visual`), matching iOS (Chrome for Developers, "Prepare for viewport resize behavior changes").

## 2. Choose resize behaviour (Chrome on Android 108+ only per MDN compat data; Firefox and desktop Chromium do not support it)
```html
<meta name="viewport" content="width=device-width, initial-scale=1, interactive-widget=resizes-content">
```
`resizes-content` shrinks the layout viewport so `dvh` units and fixed-bottom elements move above the keyboard. Values: `resizes-visual` (default), `resizes-content`, `overlays-content` (per the Chrome blog). iOS ignores it (gated: unconfirmed, source is paywalled or blocked).

## 3. VisualViewport API (Baseline since 2021-08-10: Chrome 61, Firefox 91, Safari 13)
```js
const vv = window.visualViewport;
function placeComposer() {
  const offset = window.innerHeight - vv.height - vv.offsetTop;   // keyboard + toolbar overlap
  composer.style.transform = `translateY(${-Math.max(0, offset)}px)`;
}
vv.addEventListener("resize", placeComposer);
vv.addEventListener("scroll", placeComposer);
```
Use for chat composers and bottom action bars that must hug the keyboard.

## 4. VirtualKeyboard API (Chromium only, secure contexts: run on an https origin in Chromium 156, `navigator.virtualKeyboard.overlaysContent = true` worked; on about:blank the property was absent)
```js
if ("virtualKeyboard" in navigator) navigator.virtualKeyboard.overlaysContent = true;
```
```css
.composer { bottom: env(keyboard-inset-height, 0px); }   /* parses (CSS.supports true) and resolves to 0px with no keyboard */
```
You take full control of layout around the keyboard; `navigator.virtualKeyboard.show()` only works on elements with `virtualkeyboardpolicy="manual"`.

## 5. Form UX
- Inputs >= 16px font to stop iOS zoom on focus (gated: unconfirmed, source is paywalled or blocked).
- `inputmode` and `enterkeyhint` choose the right keyboard and action key.
- After focus, ensure the field is visible: `el.scrollIntoView({ block: "center" })` on `focus` if your layout hides it.

## Verify
- [ ] On iPhone and Android, focusing the chat input keeps it and the send button visible above the keyboard; closing the keyboard restores layout.

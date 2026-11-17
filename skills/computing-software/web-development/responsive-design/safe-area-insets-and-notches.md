---
id: computing-software.web-development.responsive-design.safe-area-insets-and-notches
name: safe-area-insets-and-notches
category: computing-software
field: web-development
product: responsive-design
tags: [viewport-fit, env-safe-area, safe-area-inset, notch, home-indicator, responsive-design]
level: practitioner
status: gated
description: "Handling notches, rounded corners and home indicators: viewport-fit=cover, env(safe-area-inset-*) with max() fallbacks, fixed bars, landscape insets and standalone PWAs."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/env
  - https://webkit.org/blog/7929/designing-websites-for-iphone-x/
  - https://developer.chrome.com/docs/css-ui/edge-to-edge
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe area insets and notches

## 1. Opt in to drawing edge to edge
```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```
Without `viewport-fit=cover` the browser letterboxes the page and insets are 0 (WebKit blog: content is automatically inset within the safe area; on desktop Chromium `env(safe-area-inset-bottom)` resolved to 0px in a run). With it, your content can sit under the notch/status bar/home indicator, so you must pad it back.

## 2. Pad with env()
```css
.page {
  padding-left:  max(1rem, env(safe-area-inset-left));
  padding-right: max(1rem, env(safe-area-inset-right));
}
.bottom-bar {
  position: fixed; inset-inline: 0; bottom: 0;
  padding-bottom: calc(.75rem + env(safe-area-inset-bottom));   /* clear the iOS home indicator */
}
.top-bar { padding-top: env(safe-area-inset-top); }
```
- `env(name, fallback)` accepts a fallback; `max()` keeps your normal padding when the inset is smaller.
- Left/right insets are non-zero in landscape on notched phones (gated: unconfirmed, source is paywalled or blocked): full-width backgrounds should still extend under them; only text/controls need padding.

## 3. Where insets matter
- Fixed headers, tab bars and floating action buttons.
- Full-screen dialogs/sheets (`<dialog>` covering the viewport).
- Standalone PWAs: with `apple-mobile-web-app-status-bar-style: black-translucent` (iOS) or edge-to-edge display on Android, content runs under the status bar, so `safe-area-inset-top` matters (gated: unconfirmed, source is paywalled or blocked).
- Chrome on Android draws edge-to-edge from Chrome 135 (Chrome for Developers edge-to-edge guide) and exposes `safe-area-inset-bottom` for the gesture bar when `viewport-fit=cover` is set.

## 4. Gotchas
- Values change on rotation and when browser toolbars show/hide (Chrome edge-to-edge guide: `safe-area-inset-bottom` updates as the chin moves); use them in CSS, not measured once in JS.
- `100vh` elements plus bottom insets can overflow; use `100dvh` and inset padding.

## Verify
- [ ] On an iPhone with a notch/Dynamic Island (or Xcode Simulator), in portrait and landscape, no text or buttons sit under the notch or home indicator; fixed bars clear the home indicator.

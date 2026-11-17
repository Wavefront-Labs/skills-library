---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-webxr-dom-overlay-ar-ui
name: threejs-webxr-dom-overlay-ar-ui
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-webxr, dom-overlay, ar-ui, beforexrselect, immersive-ar]
level: practitioner
status: draft
description: "Build HTML UI for handheld AR in three.js with the WebXR DOM Overlay: setup via ARButton, beforexrselect to stop taps placing objects, layout and fallbacks."
sources: ["https://immersive-web.github.io/dom-overlays/", "https://threejs.org/docs/#examples/en/webxr/ARButton", "https://developers.google.com/ar/develop/webxr/hello-webxr"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WebXR DOM overlay and AR UI

## 1. Setup
```js
const overlay = document.getElementById('ar-ui');      // a full-screen container
document.body.appendChild(ARButton.createButton(renderer, {
  requiredFeatures: ['hit-test'], optionalFeatures: ['dom-overlay'], domOverlay: { root: overlay } }));
renderer.xr.addEventListener('sessionstart', () => {
  const type = renderer.xr.getSession().domOverlayState?.type;   // 'screen' on phones, 'floating'/'head-locked' on headsets
  overlay.hidden = false;
});
```
Only one root element and its descendants show during the session; everything else is hidden.

## 2. Stop UI taps from also selecting in XR
```js
overlay.addEventListener('beforexrselect', e => e.preventDefault());  // taps on UI do not fire 'select'
```
Without this, pressing a button also places an object via the controller `select` event.

## 3. Layout
- Fixed-position bottom bars and big touch targets (48 px+); safe-area insets (`env(safe-area-inset-bottom)`).
- Exit button calling `renderer.xr.getSession().end()`.
- Keep the overlay transparent (`background: transparent`) except UI panels; it covers the camera feed.
- Instruction states: scanning ("move your phone"), surface found, placed.

## 4. Fallbacks
`dom-overlay` is supported in Chrome for Android; headsets may show it floating or not at all.
Check `session.domOverlayState` and render UI in 3D (meshes, troika text) when absent.

## Gotchas
- `optionalFeatures` without `domOverlay.root` silently disables it.
- CSS transforms/animations on the overlay cost frame time on mid-range phones; keep them simple.
- Fullscreen elements (video) inside the overlay are not allowed.

## Verify
- [ ] Tapping UI buttons never places or moves AR content.
- [ ] Overlay hidden again after session end; page layout restored.

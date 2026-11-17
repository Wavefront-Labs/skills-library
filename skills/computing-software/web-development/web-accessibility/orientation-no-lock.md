---
id: computing-software.web-development.web-accessibility.orientation-no-lock
name: orientation-no-lock
category: computing-software
field: web-development
product: web-accessibility
tags: [info-and-relationships, orientation-lock, wcag-1-3-4, responsive-design, mobile]
level: practitioner
status: verified
description: "Meeting WCAG 1.3.4 Orientation: supporting both portrait and landscape, avoiding CSS and JS orientation locks, the essential-use exceptions, and testing rotation."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/orientation.html
  - https://developer.mozilla.org/en-US/docs/Web/API/ScreenOrientation/lock
  - https://www.w3.org/WAI/WCAG22/Techniques/failures/F97
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Orientation: don't lock portrait or landscape

**1.3.4 (AA):** content doesn't restrict its view and operation to a single display orientation unless a specific orientation is essential.

## 1. Who needs it
People with devices mounted on wheelchairs or bed frames in a fixed orientation, users who can't easily rotate a phone, people using tablets in keyboard docks.

## 2. Failures
- "Please rotate your device" messages or overlays that block content in one orientation (failure F100).
- Locking the orientation (failure F97) or CSS that hides or rotates the whole page: `@media (orientation: landscape) { body { display: none } }` or `transform: rotate(90deg)` (W3C names no CSS form specifically; offering one orientation is what fails).
- `screen.orientation.lock("portrait")` in a web app or `"orientation": "portrait"` in the web app manifest for non-essential apps (affects installed PWAs).
- Layouts that technically work but cut off controls in landscape on small phones (no scrolling because of `height: 100vh; overflow: hidden`).

## 3. Exceptions (essential)
Piano/instrument apps, bank cheque deposit photo capture, VR, presentations of a specific aspect ratio, some games. Be honest: "it looks better in portrait" isn't essential.

## 4. Implementation
- Design with fluid layouts; test landscape phone (~ 740x360 CSS px) specifically - very short viewports expose fixed headers/footers eating all space.
- Use `@media (orientation: landscape) and (max-height: 500px)` to compact chrome (smaller header, non-sticky) rather than block.
- If you suggest an orientation, show a dismissible hint, not a blocker.

## Verify
Rotate real devices and DevTools device mode (rotate button) on every key screen: all content and functions available; with OS rotation lock on, the page still works in the locked orientation.

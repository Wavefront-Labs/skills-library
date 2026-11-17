---
id: computing-software.web-development.web-accessibility.motion-actuation-alternatives
name: motion-actuation-alternatives
category: computing-software
field: web-development
product: web-accessibility
tags: [input-modalities, pointer-accessibility, motion-actuation, wcag-2-5-4, devicemotion, shake-to-undo, tilt-controls]
level: practitioner
status: docs-checked
description: "Meeting WCAG 2.5.4 Motion Actuation: UI alternatives for shake, tilt or gesture-to-camera features, and the ability to disable motion response."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/motion-actuation.html
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/devicemotion_event
  - https://developer.mozilla.org/en-US/docs/Web/API/DeviceMotionEvent/requestPermission_static
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Motion actuation alternatives

**Goal:** no function depends on moving the device or gesturing at a camera, and motion response can be turned off.

## 1. The rule (2.5.4, A)
Functions triggered by device motion (shake, tilt, rotate) or user motion (wave at camera) must:
1. also be operable through normal UI components, **and**
2. allow disabling the motion response (to prevent accidental activation - the Understanding page names fixed mounts such as a wheelchair and motor impairments).
Exceptions: the motion is used through an accessibility-supported interface, or the motion is essential for the function and removing it would invalidate the activity.

## 2. Examples
| Motion feature | UI alternative |
|---|---|
| Shake to undo | Undo button |
| Tilt to scroll / pan a panorama | Arrow buttons, drag, keyboard |
| Shake to report a bug | Menu item "Report a problem" |
| Wave to advance slides | Next/Previous buttons |

Settings toggle: "Respond to device motion: On/Off", persisted.

## 3. Implementing device motion responsibly
```js
async function enableMotion() {
  if (typeof DeviceMotionEvent?.requestPermission === 'function') {        // where the API exists it needs transient user activation
    if (await DeviceMotionEvent.requestPermission() !== 'granted') return;
  }
  window.addEventListener('devicemotion', onMotion);
}
const disableMotion = () => window.removeEventListener('devicemotion', onMotion);
```
`requestPermission()` is available only in secure contexts and needs transient user activation (MDN). Use a threshold and cooldown for shake detection to avoid accidental triggers.

## 4. Orientation is different
Screen orientation changes are covered by 1.3.4 Orientation (don't lock to portrait/landscape) - not motion actuation.

## Verify
- [ ] Every motion-triggered function has a visible control doing the same.
- [ ] Motion response can be switched off and stays off after reload.
- [ ] Shaking during normal use doesn't trigger actions when disabled.

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text of 2.5.4 Motion Actuation (Level A): operable through user interface components and motion response can be disabled, with the supported-interface and essential exceptions; the Understanding page covers shaking, tilting and camera gestures and fixed mounts. MDN confirms DeviceMotionEvent.requestPermission() needs a secure context and transient user activation. Removed the iOS version, pedometer and prefers-reduced-motion claims.

Method: documentation only; no commands were run.

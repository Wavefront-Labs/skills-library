---
id: computing-software.computer-graphics-engineering.webgl-threejs.threejs-webxr-emulator-testing
name: threejs-webxr-emulator-testing
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, threejs, three-webxr, webxr-emulator, iwer, immersive-web-emulator, remote-debugging]
level: practitioner
status: draft
description: "Test three.js WebXR apps without constant headset use: Immersive Web Emulator and IWER, Chrome remote debugging over USB/adb, HTTPS dev servers and CI smoke tests."
sources: ["https://github.com/meta-quest/immersive-web-emulator", "https://github.com/meta-quest/immersive-web-emulation-runtime", "https://developer.oculus.com/documentation/web/browser-remote-debugging/", "https://developer.mozilla.org/en-US/docs/Web/API/WebXR_Device_API/Fundamentals"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing WebXR with emulators and devices

## 1. Desktop emulation
- **Immersive Web Emulator** (Chrome/Edge extension by Meta): emulates Quest headset and
  controllers in DevTools, keyboard/mouse pose control, room-scale and AR plane/mesh simulation.
- **IWER** (`iwer` npm, Immersive Web Emulation Runtime): inject a WebXR polyfill from code for
  automated tests and dev builds:
```js
import { XRDevice, metaQuest3 } from 'iwer';
if (import.meta.env.DEV && !navigator.xr?.isSessionSupported) new XRDevice(metaQuest3).installRuntime();
```
- The older WebXR API Emulator extension (Mozilla) is unmaintained.

## 2. Secure context
WebXR needs HTTPS (or localhost). For a headset on the LAN: `vite --host` with
`@vitejs/plugin-basic-ssl`, or `adb reverse tcp:5173 tcp:5173` and open `localhost:5173` on the
Quest (no certificate needed).

## 3. On-device debugging
Quest: enable developer mode, connect USB, `adb devices`, then `chrome://inspect` on desktop
Chrome to get console, breakpoints and performance profiles from the headset browser. Android
AR: same via Chrome remote debugging. OVR Metrics Tool overlays frame timing on Quest.

## 4. Automated checks
Playwright plus IWER: start a session, set controller poses, assert scene state (object picked,
teleported). Pixel output under emulation is not representative; test logic and state, not visuals.

## Gotchas
- Emulators do not reproduce performance, foveation, reprojection or hand-tracking jitter: always profile on device.
- `isSessionSupported('immersive-ar')` differs by browser; code paths for unsupported must be tested too.
- Permission prompts and user-gesture requirements for `requestSession` still apply in emulation.

## Verify
- [ ] Entering VR in the emulator renders both eyes and controllers respond.
- [ ] Same build runs on device via adb reverse with remote DevTools attached.

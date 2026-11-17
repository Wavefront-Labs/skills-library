---
id: computing-software.general-digital-literacy.web-browsers.browser-hardware-acceleration-problems
name: browser-hardware-acceleration-problems
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [hardware-acceleration, browser-graphics, gpu-driver, video-flicker, chrome-gpu]
level: practitioner
status: draft
description: "Fix black video, flicker, freezes and crashes in a browser by toggling hardware acceleration, updating GPU drivers and checking the GPU status page."
sources: ["https://support.google.com/chrome/", "https://support.mozilla.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hardware acceleration problems in browsers

**Symptoms:** flickering or black video, green frames, page rendering glitches, browser freezing or crashing, high GPU use.

## Steps (least to most invasive)
1. Update the browser and the GPU driver from the GPU vendor (not only Windows Update). Restart.
2. Turn hardware acceleration off as a test:
   - Chrome/Edge: Settings > System > "Use graphics acceleration when available" (Edge: "Use hardware acceleration when available") > off > relaunch.
   - Firefox: Settings > General > Performance > uncheck "Use recommended performance settings", then uncheck "Use hardware acceleration when available" > restart.
3. If the problem disappears, the cause is the driver or GPU path: keep it off or update/roll back the driver; re-enable after updates to see if fixed.
4. Inspect status: `chrome://gpu` (Chrome/Edge: `edge://gpu`) shows what is hardware accelerated and any problems; Firefox: `about:support` Graphics section.
5. Try disabling extensions and test with a fresh profile to rule them out.
6. Laptops with two GPUs: set the browser to use the integrated or the discrete GPU in system graphics settings and compare.

## Trade-off
Software rendering raises CPU use and battery drain and makes video playback less smooth; treat it as a diagnostic or short-term workaround.

## Verify
Reproduce the original problem (the video or site); it stays fixed for a working session.

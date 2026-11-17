---
id: computing-software.general-digital-literacy.web-browsers.slow-browser-and-high-memory-use
name: slow-browser-and-high-memory-use
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-troubleshooting, slow-browser, memory-saver, task-manager, efficiency-mode]
level: intro
status: docs-checked
description: "Speed up a slow Chrome or Edge: find the heavy tab or extension, use Memory Saver or sleeping tabs, remove extensions, update, and reset as a last step."
sources:
  - https://support.google.com/chrome/answer/1385029
  - https://support.google.com/chrome/answer/12929150
  - https://support.microsoft.com/en-gb/topic/learn-about-performance-features-in-microsoft-edge-7b36f363-2119-448a-8de6-375cfd88ab25
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Slow browser and high memory use

**Goal:** pages scroll and load quickly again.

## Find the culprit
- **Chrome:** More > More tools > Task Manager; select Memory to sort; select a task and End process (unsaved work in that task is lost). Look for items labelled "Background page".
- **Edge:** close tabs and extensions you do not need; Microsoft lists out-of-memory as a cause of crashes and failed loads.

## Quick fixes
1. Close unused tabs (`Ctrl+W`, `Cmd+W` on Mac).
2. Turn off or remove extensions you do not use (Chrome: More > Extensions > Manage extensions).
3. Update the browser and restart it.
4. **Chrome Memory Saver:** More > Settings > Performance > Memory Saver on; levels Moderate, Balanced (recommended) or Maximum. Chrome keeps tabs active that play audio or video, share the screen, send notifications, download, hold partly filled forms, are pinned or use USB or Bluetooth. Add exceptions under "Always keep these sites active".
5. **Edge sleeping tabs:** Settings and more > Settings > System and performance > Performance > Automatically put tabs to sleep (Microsoft says tabs sleep after two hours of inactivity by default; the interval is adjustable at `edge://settings/system`).
6. Chrome Preload pages (Settings > Performance) can be turned off or set to Standard or Extended.
7. Last resort: reset settings (see resetting-browser-settings).

## Is it really the browser?
- If another browser is just as slow, suspect the network or the computer.
- Unwanted programs can cause pop-ups and slowdowns; see removing-browser-hijackers.

## Verify
- [ ] The browser task manager shows no tab or extension with constant high CPU; pages scroll smoothly.

## Checked
Date: 2026-10-27. Documentation: Chrome Help ("Speed up Google Chrome", "Personalize Chrome performance") and Microsoft Support ("Learn about performance features in Microsoft Edge"), read in October 2026. Confirmed: Task Manager path, Memory Saver path, levels and exclusions, preload setting, Edge sleeping tabs path and two-hour default. Removed as unconfirmed: Firefox and Safari steps, hardware-acceleration advice, the 8 GB RAM figure and the cached-files tip.
Method: documentation only; no commands were run.

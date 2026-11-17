---
id: computing-software.web-development.frontend-development.devtools-throttling-and-device-emulation
name: devtools-throttling-and-device-emulation
category: computing-software
field: web-development
product: frontend-development
tags: [cpu-throttling, device-emulation, network-throttling, device-mode, chrome-devtools, performance-testing]
level: practitioner
status: docs-checked
description: "Realistic testing with DevTools: CPU and network throttling presets, calibrated CPU throttling, device mode limits, request blocking, sensors and when only real devices will do."
sources:
  - https://developer.chrome.com/docs/devtools/device-mode
  - https://developer.chrome.com/docs/devtools/settings/throttling
  - https://developer.chrome.com/docs/devtools/network/reference#throttling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Throttling and device emulation

## 1. CPU throttling
Use CPU throttling, or the **calibrated** presets that approximate typical low- and mid-tier mobile devices on your machine. A fast laptop hides long tasks: always profile interactions with throttling on.

## 2. Network throttling
DevTools offers network throttling presets and custom profiles (see the throttling docs for current names). Treat it as an approximation; for accurate network tests use a dedicated tool or OS-level shaping.

## 3. Device mode
Simulates a mobile viewport and can throttle CPU and network. It cannot simulate the architecture of mobile CPUs, so use it for layout and verify on real devices.

## 4. Other useful controls
- Block a third-party script or font in DevTools to test failure modes.
- Disable the cache for first-visit tests.

## 5. A reproducible profile recipe
1. Incognito window (no extensions), DevTools docked separately.
2. CPU: a mid-tier mobile preset; network: a throttled profile; disable cache for cold load.
3. Record Performance; repeat several times and compare.

## Verify
- [ ] Performance budgets are checked under the same throttling profile in CI as in manual testing.

## Checked
2026-10-28 Confirmed on Chrome DevTools pages (throttling: calibrated presets approximating low- and mid-tier mobile devices; custom profiles; device mode: simulates a mobile viewport, can throttle CPU and network, cannot simulate mobile CPU architecture). Removed: slowdown factors, preset names, price, Lantern/simulated throttling claim, command names, shortcut paths, the 'other controls' list, repeat counts.
Method: documentation only; no commands were run.

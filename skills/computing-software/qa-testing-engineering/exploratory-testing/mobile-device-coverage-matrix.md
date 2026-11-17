---
id: computing-software.qa-testing-engineering.exploratory-testing.mobile-device-coverage-matrix
name: mobile-device-coverage-matrix
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [device-coverage-matrix, mobile-testing, device-farm, os-fragmentation, browserstack, firebase-test-lab, emulator-testing, simulator-testing]
level: practitioner
status: draft
description: "Choose mobile devices and OS versions to test: market and analytics data, fragmentation dimensions, real devices vs emulators, and device farms."
sources:
  - https://firebase.google.com/docs/test-lab
  - https://www.browserstack.com/app-automate
  - https://developer.android.com/about/dashboards
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mobile device and OS coverage

**Goal:** representative device coverage within budget.

## Dimensions that cause defects
OS version (API level / iOS version), manufacturer skin (Samsung One UI, Xiaomi MIUI/HyperOS: aggressive battery killing), screen size/density/notch/foldable, RAM (low-end devices), chipset/GPU, locale, accessibility settings (large fonts).

## Selecting
1. Analytics of your user base (or market data: StatCounter, Android distribution dashboards) by model and OS.
2. Cover: top devices by usage until ~70-80% of users; plus extremes (smallest screen, oldest supported OS, low RAM device, a foldable/tablet if supported); latest OS beta before release.
3. Use pairwise (`pict-pairwise-generation`) across OS x size x manufacturer for broader automated runs.

## Where to run
- **Emulators/simulators**: fast, for most automated tests and layout checks.
- **Real devices** in-house: a small set of tier 1 devices for manual exploratory and performance/battery checks.
- **Device farms**: Firebase Test Lab (Robo tests, instrumentation tests), AWS Device Farm, BrowserStack App Live/Automate, Sauce Labs: run Espresso/XCUITest/Appium suites across many real devices.

## Gotchas
- Emulators do not reproduce OEM-specific behaviour, camera, biometrics, real performance.
- Minimum supported OS in the store listing must be tested, or raised.

## Verify
Coverage doc with user share covered, plus last-run results per device tier.

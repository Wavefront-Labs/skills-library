---
id: creative-arts.design-for-form-and-experience.prototyping.stateful-prototypes-and-on-device-preview
name: stateful-prototypes-and-on-device-preview
category: creative-arts
field: design-for-form-and-experience
product: prototyping
tags: [stateful-prototype, device-preview, prototype-logic, conditional-prototype, mobile-preview, prototype-state, testflight]
level: practitioner
status: draft
description: "Build stateful prototypes (variables, conditions, form and cart state) and preview them on real devices via tool apps, QR links, and home-screen installs."
sources:
  - "Figma Help Center - Use variables in prototypes and Figma Mirror (help.figma.com)"
  - "ProtoPie Player and Framer Preview documentation (protopie.io, framer.com/learn)"
  - "Apple Developer - TestFlight (developer.apple.com/testflight)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stateful prototypes and on-device preview

## Why state matters
A click-through shows fixed paths; **stateful** prototypes remember what the user did (items in cart, login status, form text, toggle values), so tasks feel real and tests are valid for flows with branching.

## Implement state
- **Figma:** **variables** (boolean, number, string, colour) with **set variable** actions, **conditionals** (if/else on variables), **expressions** (increment counters, string concatenation), **variable modes** for themes and **input fields** via plugins or prototype text-input features. Build one component whose variants depend on variables.
- **ProtoPie / Framer / Axure:** variables and formulas (`creative-arts.design-for-form-and-experience.prototyping.protopie-sensor-and-variable-prototypes`), code overrides, or Axure's conditions and global variables.
- **Code (React/Vue):** a few `useState`/store values plus fixtures (`creative-arts.design-for-form-and-experience.prototyping.coded-prototypes`).
- Map the states first (**state table:** state, variable values, what the screen shows, transitions) to avoid spaghetti.

## Preview on device
- **Figma Mirror** (iOS/Android app signed into the same account) or open the prototype **share link** in a mobile browser; set **device frame and scaling** (fit to width) and hide hotspots hints off for tests.
- **ProtoPie Player** (QR/share), **Framer** preview link, **Axure Share/AxShare**, **Maze** and **UserTesting** wrappers for remote tests.
- Native-like feel: add the web prototype to the **home screen** (PWA manifest), or distribute coded builds via **TestFlight** (iOS) and Firebase App Distribution (Android) for realistic tests with sensors.
- Test with real network conditions, real screen sizes, one-handed use, and sunlight, since prototypes on a laptop hide touch and ergonomic issues.

## Checklist for sessions
Charge devices, disable notifications and auto-lock, sign in beforehand, reset prototype state between participants (reload or reset action), and have a backup device.

## Verify
- [ ] State table matches prototype behaviour; reset action exists.
- [ ] Tested on target devices, not only a desktop preview.
- [ ] Session checklist run before each participant.

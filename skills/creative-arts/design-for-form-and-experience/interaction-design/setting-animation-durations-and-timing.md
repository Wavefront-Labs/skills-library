---
id: creative-arts.design-for-form-and-experience.interaction-design.setting-animation-durations-and-timing
name: setting-animation-durations-and-timing
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [animation-duration, motion-timing, durations, ui-motion, stagger-delay, motion-design]
level: practitioner
status: draft
description: "Set UI animation durations: short for small elements, longer for large travel, use duration tokens, stagger sensibly and keep interaction feedback quick."
sources:
  - "Material Design 3 motion (m3.material.io/styles/motion)"
  - "Nielsen Norman Group, Executing UX Animations: Duration and Motion Characteristics (nngroup.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Durations and timing

Duration depends on the distance moved, the size of the element and the importance of the moment. Too fast feels abrupt; too slow makes the interface feel sluggish.

## Guidelines (starting points; test on devices)
- **Small, local changes** (hover, toggles, ripples): around 100-200 ms.
- **Medium elements** (menus, dialogs, cards expanding): around 200-300 ms.
- **Large or full-screen transitions:** around 300-500 ms.
- Leaving usually slightly faster than entering.
- Longer than about a second is rare; use it only for storytelling or onboarding.
- Nielsen Norman Group suggests that UI animations commonly sit between about 100 ms and 500 ms; verify in their article for specifics.

## Material 3 duration tokens
M3 defines tokens grouped as short, medium, long and extra long, in 50 ms steps within a range from 50 ms to 1000 ms (for example short2 is 100 ms, medium2 is 300 ms). Check the current documentation for exact values.

## Stagger and delay
Stagger lists with a small offset between items (tens of milliseconds) and cap the total sequence time; long staggers delay access to content.

## Rules
- Never block input waiting for an animation to finish.
- Scale duration with distance; do not use one value for everything.
- Test on slow devices where frame drops lengthen perceived time.

## Verify
- [ ] Durations come from named tokens.
- [ ] The longest sequence completes in well under a second for routine actions.
- [ ] Interactions remain usable during animations.

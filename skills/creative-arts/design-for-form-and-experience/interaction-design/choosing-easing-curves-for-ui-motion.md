---
id: creative-arts.design-for-form-and-experience.interaction-design.choosing-easing-curves-for-ui-motion
name: choosing-easing-curves-for-ui-motion
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [easing-curves, easing, cubic-bezier, ui-motion, motion-design, animation-curves]
level: practitioner
status: draft
description: "Choose easing curves for UI motion: ease out for entering, ease in for leaving, standard versus emphasised curves, CSS cubic-bezier values and avoiding linear."
sources:
  - "Material Design 3 motion (m3.material.io/styles/motion)"
  - "W3C CSS Easing Functions Level 1 (w3.org/TR/css-easing-1)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Easing curves

Easing describes how speed changes over an animation. Real objects accelerate and decelerate, so linear motion feels mechanical except for continuous loops (spinners, progress).

## Rules of thumb
- **Entering** (appearing on screen): decelerate (ease out): fast start, soft landing.
- **Exiting:** accelerate (ease in): slow start, leaving fast.
- **Moving within the screen** (between positions): ease in-out or a standard curve.
- Use **one family of curves** for the product so motion feels consistent.

## CSS keywords
`ease` is cubic-bezier(0.25, 0.1, 0.25, 1); `ease-in` is (0.42, 0, 1, 1); `ease-out` is (0, 0, 0.58, 1); `ease-in-out` is (0.42, 0, 0.58, 1). `linear` has no acceleration.

## Material Design 3 curves (published values)
Standard cubic-bezier(0.2, 0, 0, 1); standard decelerate (0, 0, 0, 1); standard accelerate (0.3, 0, 1, 1); emphasized decelerate (0.05, 0.7, 0.1, 1); emphasized accelerate (0.3, 0, 0.8, 0.15). Emphasized motion uses a longer, more expressive path for hero moments. Check the current Material 3 documentation for changes.

## Springs
Spring animation (iOS and others) uses stiffness and damping instead of duration; useful for gesture-driven motion, because it keeps velocity after release.

## Tools
Chrome DevTools cubic-bezier editor, cubic-bezier.com, Figma smart animate easing options (see `...figma.smart-animate-in-figma-prototypes`).

## Verify
- [ ] Entering elements ease out; leaving elements ease in.
- [ ] The product uses a small set of named curves.
- [ ] Nothing important uses linear easing except loops.

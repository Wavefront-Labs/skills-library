---
id: creative-arts.design-for-form-and-experience.figma.smart-animate-in-figma-prototypes
name: smart-animate-in-figma-prototypes
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [smart-animate, figma-animation, transitions, easing, spring-animation, prototype-animation, micro-interactions, figma]
level: practitioner
status: docs-checked
description: "Use Smart animate in Figma: layer matching rules, animatable properties, easing and springs, and troubleshooting layers that jump or dissolve."
sources:
  - https://help.figma.com/hc/en-us/articles/360039818874-Smart-animate-layers-between-frames
  - https://help.figma.com/hc/en-us/articles/360040522373-Prototype-animations
  - https://help.figma.com/hc/en-us/articles/360051748654-Prototype-easing-and-spring-animations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Smart animate

**Goal:** animate between two frames so matching layers interpolate smoothly.

## How matching works
Smart animate pairs layers across frames using **layer name and position in the hierarchy**. Matched layers animate changes in **scale (size), position, opacity, rotation and fill** (solid, gradient, image). New layers in the destination frame dissolve in.

## Setup
1. Duplicate the frame so both states contain the layers you want to animate; duplicating keeps names consistent.
2. Keep names identical and the hierarchy the same.
3. Set the connection's transition to **Smart Animate** and choose **Duration** and **Easing**.
4. Easing is either a Bezier curve (Linear, Ease In, Ease Out, Ease In And Out and the three "Back" variants, or **Custom bezier**) or a spring (**Gentle, Quick, Bouncy, Slow, Custom**). Custom spring exposes Stiffness (number of bounces), Damping (level of spring) and Mass (speed and bounce height).
5. Ease Out suits moving objects into view; Ease In suits moving them out.
6. To fade opacity, set the layer opacity to 0% rather than toggling visibility.

## Limits and troubleshooting
- Unsupported properties (drop shadow, inner shadow, moving between different shape types) make Figma fall back to a default **dissolve**.
- Smart animate is not supported for overlay actions.
- **Layer dissolves or jumps:** names differ between frames, or duplicated layers are mismatched; fix the names (unique names help) and compare by selecting the layer, which Figma highlights in other frames where it exists.
- Increase the duration while building so you can see what is matching.
- Respect reduced motion in real products; prototype the reduced alternative as a separate flow (`creative-arts.design-for-form-and-experience.interaction-design.designing-component-states-and-micro-interactions`).

## Verify
- [ ] Matching layers share name and hierarchy.
- [ ] No unexpected dissolves on playback.

## Checked
2026-11-01. Confirmed against the three Help Center pages above: matching by name and hierarchy, animatable properties, dissolve fallback and overlay limit, easing and spring option names, custom spring parameters, entering/exiting easing advice. Removed: default durations in ms, text and corner-radius/effects animation claims, same-type matching rule, variant and After delay/Drag claims, auto layout and performance claims, pattern list and the Material Design source (not read).
Method: documentation only; no commands were run.

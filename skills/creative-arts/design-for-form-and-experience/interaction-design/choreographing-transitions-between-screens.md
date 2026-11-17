---
id: creative-arts.design-for-form-and-experience.interaction-design.choreographing-transitions-between-screens
name: choreographing-transitions-between-screens
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [transition-choreography, shared-element-transition, container-transform, ui-transitions, motion-choreography, motion-design]
level: practitioner
status: draft
description: "Choreograph screen transitions: preserve context with shared elements and container transforms, order and stagger movements and keep the hierarchy clear."
sources:
  - "Material Design 3 motion (m3.material.io/styles/motion)"
  - "Apple Human Interface Guidelines, Motion (developer.apple.com/design/human-interface-guidelines)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Transition choreography

Choreography coordinates the animation of several elements so the change between states explains what happened.

## Principles
- **Maintain continuity:** keep an element visually connected across views (a shared element or container transform) so users see where it went.
- **Establish hierarchy:** the primary element moves first or most prominently; secondary elements follow.
- **Direct attention:** motion leads the eye to the new focus.
- **Keep the spatial model consistent:** if a panel slides in from the right, it leaves to the right.
- **Be consistent:** the same pattern for the same navigation type.

## Patterns
- **Container transform:** a card expands into a detail page; content cross-fades inside the moving container.
- **Shared axis:** screens at the same level slide along an axis with a fade.
- **Fade through:** unrelated views fade out then in.
- **Shared element:** one element (an image) flies from one screen to the next.
- **Stagger:** list items enter in sequence.

## Build
1. Storyboard the start and end frames; mark which elements persist, enter and leave.
2. Sequence with small offsets (see `...interaction-design.setting-animation-durations-and-timing`) and easing (see `...interaction-design.choosing-easing-curves-for-ui-motion`).
3. Prototype in Figma Smart Animate (see `...figma.smart-animate-in-figma-prototypes`) or code (View Transitions API, native transitions); test back navigation too.
4. Provide a reduced-motion version.

## Verify
- [ ] A persistent element is visually tracked across the change.
- [ ] Back navigation reverses the motion.
- [ ] Reduced-motion users get a simple fade or instant change.

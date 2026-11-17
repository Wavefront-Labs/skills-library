---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-reduced-motion-alternatives
name: designing-reduced-motion-alternatives
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [reduced-motion-design, prefers-reduced-motion, reduced-motion, motion-sensitivity, vestibular-accessibility, wcag-2-3-3]
level: practitioner
status: draft
description: "Design reduced-motion alternatives: respect the OS setting, replace large movement with fades, stop auto-play, and meet WCAG motion criteria."
sources:
  - "W3C WCAG 2.2 (w3.org/TR/WCAG22)"
  - "W3C CSS Media Queries Level 5, prefers-reduced-motion (w3.org/TR/mediaqueries-5)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Reduced motion alternatives

Large or looping motion can trigger dizziness, nausea or headaches (vestibular disorders) or distract people with attention differences. Provide alternatives.

## Standards
- **WCAG 2.3.3 Animation from Interactions (AAA):** motion animation triggered by interaction can be disabled unless it is essential.
- **WCAG 2.2.2 Pause, Stop, Hide (A):** moving, blinking or scrolling content that starts automatically and lasts more than five seconds needs a mechanism to pause, stop or hide it (with exceptions).
- **WCAG 2.3.1 Three Flashes or Below Threshold (A):** no content flashes more than three times in one second beyond the thresholds.

## Implementation
- CSS: `@media (prefers-reduced-motion: reduce) { ... }` to replace or remove animations; in JavaScript, `window.matchMedia('(prefers-reduced-motion: reduce)')`. iOS has Reduce Motion; Android has "Remove animations"; Windows and macOS have equivalents.
- **Do not remove all feedback;** replace motion with a non-motion cue: cross-fade, a colour or opacity change, or an instant state change.
- Reduce or remove: parallax, large zooms, spinning, sliding across the whole screen, auto-playing video or carousels, and bouncing.
- Allow essential motion that conveys information (a progress indicator) but make it small and slow.
- Provide an in-app toggle if the OS setting may not reach users.

## Design
Spec two versions for each motion in the motion spec (see `...interaction-design.writing-a-motion-spec-for-handoff`): default and reduced.

## Verify
- [ ] Enabling the OS setting removes large movement across the product.
- [ ] Autoplay stops or can be paused.
- [ ] Information is still conveyed without motion.

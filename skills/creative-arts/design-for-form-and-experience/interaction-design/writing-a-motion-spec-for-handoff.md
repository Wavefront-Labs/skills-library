---
id: creative-arts.design-for-form-and-experience.interaction-design.writing-a-motion-spec-for-handoff
name: writing-a-motion-spec-for-handoff
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [motion-spec, motion-specification, animation-spec, motion-handoff, ui-motion, motion-documentation]
level: practitioner
status: draft
description: "Write a motion spec developers can build: trigger, properties, start and end values, duration, easing, delay, orchestration and reduced-motion variant."
sources:
  - "Material Design 3 motion (m3.material.io/styles/motion)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Motion specs for handoff

A prototype shows the feel; a spec gives numbers a developer can implement and QA can check.

## Contents for each animation
1. **Name and purpose** (what it communicates).
2. **Trigger:** user action or system event; what interrupts it.
3. **Elements and properties animated:** position, scale, opacity, colour, corner radius, clip.
4. **Start and end values** in design units (px or dp, percent) and the anchor or transform origin.
5. **Duration** and **delay** (use tokens, see `...interaction-design.setting-animation-durations-and-timing`).
6. **Easing** (a named curve or cubic-bezier values; for springs, stiffness and damping and mass).
7. **Orchestration:** order, offsets and what runs in parallel; a timeline chart with bars per element.
8. **Interruption and reverse behaviour:** what happens if the user cancels or navigates mid-way.
9. **Reduced-motion variant** (see `...interaction-design.designing-reduced-motion-alternatives`).
10. **Platform notes:** the native API or library to use (CSS, Web Animations API, Lottie, native transitions).

## Deliver
A page in the design file with keyframe frames and a table; a short screen recording (a clip with timeline) and, where useful, a Lottie or a reference implementation. Review with developers and measure the built version against the spec.

## Verify
- [ ] Durations and easings reference tokens or exact values.
- [ ] Interruption is specified.
- [ ] A reduced-motion version exists.

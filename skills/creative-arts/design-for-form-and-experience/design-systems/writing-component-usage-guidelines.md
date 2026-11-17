---
id: creative-arts.design-for-form-and-experience.design-systems.writing-component-usage-guidelines
name: writing-component-usage-guidelines
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [usage-guidelines, design-system-documentation, dos-and-donts, component-documentation, content-guidelines, accessibility-guidelines, design-docs]
level: practitioner
status: draft
description: "Write component usage guidelines: purpose, anatomy, variants, do and don't examples, content rules, accessibility, behaviour and related components, in a consistent template."
sources:
  - "Nathan Curtis (EightShapes), Documenting Components (medium.com/eightshapes-llc)"
  - "Atlassian Design System - Component pages (atlassian.design/components)"
  - "Gov.uk Design System component template (design-system.service.gov.uk/components)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Component usage guidelines

**Goal:** a team can pick, configure and use a component correctly without asking the system team.

## Template (same sections every time)
1. **Overview:** one-sentence purpose and a live example.
2. **When to use / when not to use,** with alternatives ("Use a toast for transient feedback; use an inline alert for persistent messages").
3. **Anatomy:** labelled diagram of parts (container, label, icon, helper text) with names matching the code and Figma layers.
4. **Variants and states:** type, size, emphasis; default, hover, focus, pressed, disabled, loading, error, read-only; show each.
5. **Do and Don't pairs:** side-by-side images with captions, 3-6 pairs; real content, not lorem ipsum.
6. **Content:** label length, capitalisation, voice, truncation rules (`creative-arts.design-for-form-and-experience.ux-design.writing-microcopy-and-button-labels`).
7. **Behaviour:** responsive rules, interaction, motion, keyboard.
8. **Accessibility:** role, ARIA attributes, keyboard map, focus order, contrast notes, screen reader announcements, WCAG criteria met.
9. **Layout and spacing** specs (tokens, not pixels), placement guidance.
10. **Related components** and patterns; code API link; Figma link; changelog and status.

## Writing tips
- Prescriptive but brief; link rather than repeat.
- Tie guidance to evidence (research, support tickets).
- Write for designers and developers both; separate tabs for Design and Code.
- Review docs with a new user performing a task with no help.

## Verify
- [ ] All sections present and consistently named.
- [ ] Each do has a matching don't with a reason.
- [ ] Accessibility section lists keyboard, ARIA and contrast.

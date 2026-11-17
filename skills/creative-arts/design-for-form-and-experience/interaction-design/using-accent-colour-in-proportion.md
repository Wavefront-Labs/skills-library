---
id: creative-arts.design-for-form-and-experience.interaction-design.using-accent-colour-in-proportion
name: using-accent-colour-in-proportion
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [accent-color-use, ui-color, color-proportion, 60-30-10, brand-color, color-in-interfaces]
level: practitioner
status: draft
description: "Apply accent colour in UI proportion: mostly neutrals, one brand accent for primary actions and key signals, with roles for each colour and a limit on competing hues."
sources:
  - "Material Design 3 - Color roles and the accent / surface system (m3.material.io/styles/color/roles)"
  - "Refactoring UI, Wathan and Schoger (2018), working with colour"
  - "Apple Human Interface Guidelines - Color (developer.apple.com/design/human-interface-guidelines/color)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Accent colour and proportion

**Goal:** colour guides attention and meaning because it is scarce and consistent.

## Proportion
Roughly **60 percent neutral surface, 30 percent secondary/neutral content, 10 percent accent** is a design heuristic, not a rule. The point: the accent is rare enough to stand out.

## Role-based colour
- **Neutrals** (surface, background, text, borders): a grey ramp of 8-10 steps.
- **One brand accent** for the primary action, selected state, links, focus ring and key data highlight. Use it for the single most important action per screen.
- **Secondary accent** (optional) for charts or tags, never competing with primary buttons.
- **Semantic colours** for status (see `creative-arts.design-for-form-and-experience.interaction-design.designing-status-and-semantic-colours`) are kept separate from brand colour.
- Material 3 formalises roles: primary, on-primary, primary-container, secondary, tertiary, surface, outline.

## Practice
1. Convert the design to greyscale; hierarchy should still read; add colour last.
2. Put the accent on interactive and meaningful things only; decoration in neutrals.
3. Check **contrast**: accent text on white 4.5:1 (UI component 3:1); text on accent fills 4.5:1.
4. Limit hues to brand + status; extra data hues come from the chart palette.
5. Keep one colour meaning one thing; do not use the brand colour also as "error" or "success".

## Verify
- [ ] Greyscale version holds hierarchy.
- [ ] One primary accent action per view; accent used consistently for interactivity.
- [ ] Accent pairings pass contrast thresholds.

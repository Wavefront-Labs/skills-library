---
id: creative-arts.design-for-form-and-experience.design-systems.defining-a-spacing-scale
name: defining-a-spacing-scale
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [spacing-tokens, spacing-system, spacing-scale, 4pt-grid, 8pt-grid, layout-spacing, design-tokens]
level: practitioner
status: draft
description: "Define a spacing scale on a 4 or 8 pt base: named steps, usage rules for padding, gaps and layout, density-aware tokens, and enforcement in Figma and code."
sources:
  - "Material Design 3 - Layout and spacing (m3.material.io/foundations/layout)"
  - "Atlassian Design System - Spacing tokens (atlassian.design/foundations/spacing)"
  - "Brad Frost - Atomic Design and spacing, and Refactoring UI, Wathan and Schoger (2018)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spacing scale and tokens

**Goal:** consistent whitespace through a small set of values used everywhere.

## Choose the base
- **4 px base** with a mostly-8 scale: 0, 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96. Keep about 10-12 steps; each about 1.25-1.5x the previous at larger sizes.
- Name by step (`space-100` = 8 px, or t-shirt `space-sm`) rather than by value, so values can change; Atlassian uses `space.100` = 8 px.
- Use **rem**-based values (0.25rem multiples) in code so spacing scales with text zoom when appropriate.

## Rules of use
1. **Inside components** (padding): 8-16 px; related items gap 4-8; **between components** 16-24; **between sections** 32-64; page margins 16/24/32.
2. **Proximity encodes relationship:** smaller space for related items, larger between groups (`creative-arts.design-for-form-and-experience.interaction-design.grouping-with-gestalt-principles`).
3. **Use gap/stack primitives:** `gap` in flex/grid, a `Stack` component with a `space` prop, instead of per-element margins; avoid margin collapsing surprises.
4. **Icons and text** share the same baseline; icon-to-label gap 4-8 px.
5. **Line heights** on a 4 px grid (16, 20, 24, 28...) to keep vertical rhythm.
6. **Density:** compact modes shift tokens down one step (`creative-arts.design-for-form-and-experience.design-systems.designing-density-modes`).

## Enforcement
- Figma: variables for spacing bound to auto layout padding and gap; nudge amount 8 (and 1 with shift 4); lint with plugins.
- Code: CSS custom properties or Tailwind scale; stylelint rule banning raw px for spacing; Storybook visual checks.

## Verify
- [ ] Only scale values appear in designs and code.
- [ ] Group gaps are larger than within-group gaps.
- [ ] Tokens named by step and bound to variables.

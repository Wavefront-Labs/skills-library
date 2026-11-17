---
id: creative-arts.design-for-form-and-experience.interaction-design.writing-specs-and-redlines-for-developers
name: writing-specs-and-redlines-for-developers
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [redlines, design-specs, spec-sheet, measurements-and-specs, design-handoff, developer-handoff]
level: practitioner
status: draft
description: "Write design specs and redlines developers can build from: spacing, sizes, tokens, typography, states, responsive rules, with the minimum needed and a source of truth."
sources:
  - "Nielsen Norman Group topics (nngroup.com/topics)"
  - "Figma Help Center (help.figma.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Specs and redlines

Redlines are annotated measurements (the red lines marking spacing and sizes) used to communicate exact layout. Today most teams rely on inspected values in the design tool plus tokens, and add explicit specs only where the code cannot infer intent.

## Principles
- **Prefer tokens and components over pixel values.** If the design uses design-system components and tokens, say so; do not respecify what the system defines (see `...design-systems.writing-component-usage-guidelines`).
- **Spec what the design file cannot show:** responsive behaviour, states, truncation, minimum and maximum sizes, min and max content, animation (see `...interaction-design.writing-a-motion-spec-for-handoff`), and interaction logic (see `...interaction-design.specifying-interaction-behaviour-for-handoff`).
- **Name spacing and sizes with scale values** (space-4, radius-md), not arbitrary numbers.

## Contents
1. Layout: grid, margins, gutters, spacing between blocks, alignment rules, what stretches and what is fixed.
2. Typography: style tokens, truncation, wrapping.
3. Colour: token names, not hex.
4. States and variants: default, hover, focus, active, disabled, loading, error, empty.
5. Responsive notes per breakpoint.
6. Assets: icon names, export formats and sizes.
7. Accessibility annotations (see `...interaction-design.annotating-designs-for-accessibility`).

## Deliver
Mark frames "Ready for dev" in Figma (see `...figma.using-ready-for-dev-status-and-compare-changes`), link the spec in the ticket, and be available for questions during build.

## Verify
- [ ] A developer can build the screen from tokens, components and the notes.
- [ ] Every non-obvious behaviour is written down.
- [ ] No hex values or pixel values duplicate token definitions.

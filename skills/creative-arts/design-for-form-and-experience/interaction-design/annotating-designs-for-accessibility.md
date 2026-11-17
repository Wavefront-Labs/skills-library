---
id: creative-arts.design-for-form-and-experience.interaction-design.annotating-designs-for-accessibility
name: annotating-designs-for-accessibility
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [accessibility-annotations, a11y-annotations, accessibility-handoff, annotation-kit, accessible-design-specs, design-annotations-a11y]
level: practitioner
status: draft
description: "Annotate designs for accessibility so developers get what they need: landmarks, headings, reading and focus order, names, roles, states, alt text and keyboard behaviour."
sources:
  - "W3C WCAG 2.2 (w3.org/TR/WCAG22)"
  - "W3C WAI-ARIA Authoring Practices Guide (w3.org/WAI/ARIA/apg)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Accessibility annotations for handoff

Visual designs hide what assistive technology needs. Annotations make that information explicit before build, when it is cheap.

## What to annotate
- **Landmarks and headings:** regions (header, nav, main, aside, footer) and heading levels.
- **Reading and focus order:** numbered path across the screen; where focus moves after actions (modals, errors, new content).
- **Accessible names:** for icon-only buttons, links ("Read more" in context), inputs, images (alt text or "decorative").
- **Roles and states:** custom components and their ARIA pattern (tab, menu, dialog, switch); expanded, selected, current, disabled.
- **Keyboard behaviour:** keys supported and what they do (see `...interaction-design.designing-keyboard-operability-and-focus-order`).
- **Live regions:** which updates are announced and politeness.
- **Colour and contrast notes,** target sizes, text resize and reflow behaviour, motion and reduced-motion variants.
- **Form details:** labels, instructions, error text, autocomplete values.

## How
Use annotation components or kits (several are published for Figma by accessibility teams and vendors; choose one your team trusts), or a standard layer in the file: numbered markers with a side table. Keep one source of truth that is linked from Dev Mode (see `...figma.using-annotations-and-measurements-in-dev-mode`).

## Review
Run an accessibility review of the annotated design with an engineer before sprint planning; track annotations as acceptance criteria in tickets.

## Verify
- [ ] Each screen has focus order, names and heading levels annotated.
- [ ] Custom components cite the pattern they follow.
- [ ] Annotations are part of the ticket's acceptance criteria.

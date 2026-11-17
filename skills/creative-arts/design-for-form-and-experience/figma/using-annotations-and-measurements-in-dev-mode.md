---
id: creative-arts.design-for-form-and-experience.figma.using-annotations-and-measurements-in-dev-mode
name: using-annotations-and-measurements-in-dev-mode
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [figma-annotations, dev-mode-annotations, measurements, annotation-tools, design-notes, dev-mode-handoff]
level: practitioner
status: draft
description: "Add annotations and measurements in Figma so developers see behaviour and spacing: note categories, pinned properties, measurement tool and keeping notes current."
sources:
  - "Figma Help Center (help.figma.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Annotations and measurements

Figma Dev Mode shows annotations and measurements that designers add, and lets developers view them next to the Inspect panel.

## Annotations
- Designers add **annotations** to a layer to describe behaviour, content rules, accessibility needs or implementation notes; categories (such as interaction, accessibility, content) can be used to organise them.
- Annotations can **pin properties** (for example a specific spacing, a corner radius or a variable) so developers see the value highlighted.
- Annotation features have changed across releases; confirm the controls and plan availability in the Help Center.

## Measurements
- Add **measurements** between layers to call out distances, or rely on the automatic spacing readout when selecting and hovering.
- Measure to show required gaps that are part of a rule (a minimum gap between an icon and label), not every distance.

## Practice
1. Annotate what is not visible: behaviour, validation, truncation, responsive rules, accessibility notes (see `...interaction-design.annotating-designs-for-accessibility`).
2. Prefer tokens in annotations (`space-4`) to pixel values.
3. Keep annotations in the same frame as the design so they move with it.
4. Review annotations in the handoff conversation; remove stale ones.

## Verify
- [ ] Every non-obvious behaviour has an annotation.
- [ ] Annotations name tokens, not duplicate raw values.
- [ ] Developers can find them in Dev Mode.

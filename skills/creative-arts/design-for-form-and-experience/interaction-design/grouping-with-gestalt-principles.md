---
id: creative-arts.design-for-form-and-experience.interaction-design.grouping-with-gestalt-principles
name: grouping-with-gestalt-principles
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [gestalt-principles, visual-hierarchy, ui-layout, proximity, similarity, grouping, visual-design]
level: practitioner
status: draft
description: "Group and organise interface elements with Gestalt principles: proximity, similarity, common region, alignment, continuity and figure-ground, checked with a blur test."
sources:
  - "Nielsen Norman Group - Gestalt Principles for Visual UI Design / Proximity Principle (nngroup.com/articles/gestalt-proximity)"
  - "Wertheimer, Laws of Organization in Perceptual Forms (1923)"
  - "Lidwell, Holden and Butler, Universal Principles of Design (Rockport, 2010)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gestalt grouping in UI layout

**Goal:** make relationships and hierarchy visible through layout, with fewer lines and boxes.

## Principles and how to use them
- **Proximity:** things close together are related. Put a label nearer its field than the field above (for example 4-8 px to its own field, 16-24 px to the previous one). Use spacing steps to express levels: tight within a group, looser between groups.
- **Similarity:** same colour, size, shape means same role. All links share one style; primary buttons share one style; do not reuse the link style for decoration.
- **Common region:** an enclosing card, background or border groups content and overrides proximity. Use sparingly; a card around everything groups nothing.
- **Alignment and continuity:** shared left edges form invisible lines the eye follows; align labels, inputs and body text to the same grid lines.
- **Figure-ground:** foreground content must separate from background with contrast, elevation or blur (modals with a scrim).
- **Closure and focal point:** the eye completes shapes and lands on the item that differs; keep only one thing different at a time.

## Procedure
1. List the groups the user needs to perceive (shipping address vs payment).
2. Apply proximity first, then similarity, and add borders or backgrounds only if still unclear.
3. **Squint or blur test:** blur the screen (Figma Layer blur, or a small thumbnail). The groups should still read; if not, adjust spacing and contrast.
4. Check consistency across screens (`creative-arts.design-for-form-and-experience.design-systems.design-tokens-and-a-modular-type-scale` for spacing tokens).

## Gotchas
- Equal spacing everywhere destroys proximity cues.
- Lines and boxes everywhere add noise; remove them and see if grouping survives.

## Verify
- [ ] Groups survive the blur test.
- [ ] Gaps between groups are visibly larger than inside groups.
- [ ] Same-role elements look the same; different roles look different.

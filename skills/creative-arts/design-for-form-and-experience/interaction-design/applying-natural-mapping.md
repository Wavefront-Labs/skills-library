---
id: creative-arts.design-for-form-and-experience.interaction-design.applying-natural-mapping
name: applying-natural-mapping
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [natural-mapping, mapping, design-of-everyday-things, norman-principles, controls-and-displays, interaction-design]
level: practitioner
status: draft
description: "Apply natural mapping so controls relate spatially or conceptually to what they affect: stove-burner layouts, slider direction, and screen-to-world correspondence."
sources:
  - "Don Norman, The Design of Everyday Things, revised ed. (Basic Books, 2013), chapter 3 Knowledge in the Head and in the World (natural mapping)"
  - "Nielsen Norman Group - Mapping and Signifiers (nngroup.com)"
  - "Interaction Design Foundation - Mapping in interaction design (interaction-design.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Natural mapping

**Goal:** the relationship between a control and its effect is obvious from layout, so users do not need labels or memory.

## Levels of mapping (strongest first)
1. **Direct spatial analogy:** controls laid out like the thing controlled. Four burner knobs arranged in the same square as the burners; light switches in the same order as the lights; a seat-shaped button cluster on a car door.
2. **Directional:** up/right increases, down/left decreases; clockwise raises volume. Reverse mapping (a slider where right means less) causes errors.
3. **Cultural or conceptual:** red for hot, a thumbs-up for like. Culture-dependent, so test it.

## Applying it to interfaces
- Place a control **next to** what it changes (inline edit pencils, field-level actions, slider next to the preview) rather than in a distant toolbar.
- Order buttons the way the process runs and the way things are listed (steps left to right in left-to-right languages).
- Align sliders and bars with the data axis (higher is up).
- On maps and floor plans, orient the view to the user's heading; rotate with them.
- For a thermostat or lamp, show the result (colour swatch, temperature) on the control itself.
- Mirror the physical world in IoT apps: list lights in the room layout, not alphabetically.

## Gotchas
- Mapping fails when the layout differs from the controlled object (a stovetop with staggered burners and a linear knob row). Fix by changing the layout or adding strong labels and highlights.
- RTL languages flip horizontal mappings.

## Verify
- [ ] A new user can predict which control affects which element without labels.
- [ ] Direction conventions are consistent (up/right means more).

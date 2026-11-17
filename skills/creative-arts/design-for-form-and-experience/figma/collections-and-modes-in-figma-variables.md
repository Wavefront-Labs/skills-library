---
id: creative-arts.design-for-form-and-experience.figma.collections-and-modes-in-figma-variables
name: collections-and-modes-in-figma-variables
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [variable-modes, figma-variables, variable-collections, figma-modes, theming-in-figma, variables]
level: practitioner
status: docs-checked
description: "Organise Figma variables in collections and modes: types, one collection per concern, modes for theme and density, and publishing."
sources:
  - https://help.figma.com/hc/en-us/articles/15343107263511-Overview-of-variables-collections-and-modes
  - https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Collections and modes

Figma variables store reusable values. **Collections** group variables; **modes** give a variable several definitions, one per mode (for example light and dark), so a parent frame's mode switches the value.

## Types
- **Color:** solid fills, gradient stops, strokes, colour styles, shadow colours.
- **Number:** font size, gap, corner radius, layer opacity, stroke weight.
- **String:** text content, font family, font weight and style.
- **Boolean:** layer visibility.
- **Timing** and **Easing:** animation values in Figma Motion.
Variables are available on all plans; publishing variables to team libraries needs Professional, Education, Organization, Government or Enterprise.

## Set up
1. Create a collection per concern (primitives, semantic or theme, spacing and radius).
2. Add modes where values must change by context; the number of modes per plan is not stated on these pages, so check the current Help Center before designing around a count.
3. Use groups to organise variables; the Libraries picker can search by variable name or group (see `...design-systems.naming-design-tokens`).
4. Apply variables to the properties above and test each mode.
5. Publish the library so consumers get the collections (see `...figma.publishing-and-updating-a-figma-library`).
6. When pasting unpublished variables across files, they are copied into a new collection; if the destination has a collection and variables with identical names they are remapped.

## Practice (convention)
- Keep primitives in a collection without modes and semantic variables with modes that alias primitives (see `...figma.aliasing-variables-in-figma`).
- Name modes for what they are (Light, Dark).

## Verify
- [ ] Each mode has a value for every variable.
- [ ] A frame set to a mode changes all themed elements.
- [ ] Spacing and radius are variables, not literals.

## Checked
2026-11-01. Confirmed on the Figma Help Center pages Overview of variables, collections and modes, and Guide to variables: variable types and their properties, mode concept, all-plans availability, publishing plans, paste behaviour, search by group. Removed: mode count by plan, the frame mode control location and nested overrides, slash-name hierarchy rules, since neither page stated them.
Method: documentation only; no commands were run.

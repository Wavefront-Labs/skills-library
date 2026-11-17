---
id: creative-arts.design-for-form-and-experience.figma.nested-instances-and-instance-overrides
name: nested-instances-and-instance-overrides
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [preferred-values, instance-overrides, figma-components, nested-instances, instance-swap, reset-overrides, figma]
level: practitioner
status: draft
description: "Work with Figma nested instances, preferred values for instance swaps and instance overrides: what persists, how to reset, swap and propagate main component changes safely."
sources:
  - "Figma Help Center - Swap components and instances; Component properties; Preferred values (help.figma.com/hc/en-us/articles/360056440594)"
  - "Figma Help Center - Reset and edit instances (help.figma.com)"
  - "Figma Help Center - Nested instances (help.figma.com/hc/en-us/articles/360038662654)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nested instances, preferred values and overrides

## Nested instances
A **nested instance** is an instance inside a main component (icon inside a button, avatar inside a list item). Edit the nested instance's **properties** from the parent instance via the properties panel; changes to the nested main component propagate everywhere.
- **Expose nested instances** (the layer icon "Show nested instance properties") to reveal their properties in the parent.
- Hide, show, or swap them with boolean and instance-swap component properties (`creative-arts.design-for-form-and-experience.figma.auto-layout-components-and-variants`).

## Preferred values
For an **instance-swap property**, set **preferred values**: a curated list of components designers can swap in (the icon set subset: `Icon/Add`, `Icon/Close`, `Icon/Search`). Prevents random swaps and speeds selection. Add preferred components (or whole component sets, or styles for fills) from the property's menu.

## Instance overrides
Overrides are changes made in an instance that differ from its main: text content, fills, strokes, sizes of fill layers, visibility, swapped nested instances, effects, and variants.
- **Persistence:** overrides survive main component updates for properties not changed in the main; if you change the **same** property in the main, the **instance override wins until reset** (text set in instance stays).
- **Reset:** right-click, **Reset all overrides**, or use the reset icon beside a changed property; **Reset layer** for one layer.
- **Selection of the main:** **Go to main component** (Ctrl/Cmd+Alt+K to create; the diamond icon to select).
- Renaming layers or reordering inside the main can **break overrides** on instances; change structure deliberately, and check with the **Review changes** diff in the library (`creative-arts.design-for-form-and-experience.figma.publishing-and-updating-a-figma-library`).
- **Swap instance:** replace with another component while attempting to keep overrides (matches by layer name); keep naming consistent across components for smooth swaps.

## Practice
1. Never detach; override or request a new property.
2. Expose only the properties users need; keep names clear (Label, Icon leading, Has helper text).
3. Test in a sample screen: change text, swap icon, toggle visibility, resize.

## Verify
- [ ] Nested instance properties are exposed and preferred values set.
- [ ] Overrides survive a main update in tests; reset works.
- [ ] Layer names consistent for swapping.

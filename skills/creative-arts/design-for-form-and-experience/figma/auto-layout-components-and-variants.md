---
id: creative-arts.design-for-form-and-experience.figma.auto-layout-components-and-variants
name: auto-layout-components-and-variants
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [figma, auto-layout, frames, hug-contents, fill-container, fixed-size, padding, gap, spacing, nested-auto-layout, constraints, components, main-component, instances, overrides, variants, component-properties, boolean-property, instance-swap, text-property, variables, modes, team-library, publishing, detach-instance, responsive-design, ui-design, design-systems, dev-mode]
level: practitioner
status: draft
description: "Build resizable, reusable UI in Figma: auto layout with hug/fill/fixed sizing, nested stacks, components and instances, variants with properties, and the overrides that break when you detach."
sources:
  - "Figma Help Center: Guide to auto layout; Create and use variants; Component properties; Variables"
  - "Figma Config talks and Figma's official YouTube tutorials on auto layout and components"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Auto layout, components and variants in Figma

**Goal:** build UI that **resizes itself** when text or content changes, and that's made
from **reusable components** whose variants cover every state — so a change to the main
component updates every screen.

> **Status: draft.** Written against Figma's model as of 2024–2026 (auto layout v5 with
> wrap and min/max, component properties, variables). Figma updates frequently; menu names
> and shortcuts may move — check the Help Center for your version.

## 1. Auto layout basics
Select layers or a frame and press **Shift+A** to add auto layout. A frame becomes a
stack, like CSS flexbox.
- **Direction:** vertical, horizontal, or **wrap** (items flow to new rows).
- **Gap** between items and **padding** inside the frame — use your spacing scale (4/8/12/16…).
- **Alignment:** 9-point alignment grid in the right panel; "space between" distributes items.
- **Sizing per layer** (the crucial bit):
  - **Hug contents** — frame shrinks/grows to fit children (buttons, tags).
  - **Fill container** — child stretches to take available space (input fields, cards in a row).
  - **Fixed** — set width/height.
  - **Min/max width/height** — limits for responsive behaviour.
- **Absolute position** lets one child (a badge, close icon) ignore the flow.

**Build from the inside out:** a button = icon + label in a horizontal auto layout (hug);
a card = image + text stack (vertical) + button row (horizontal), all nested. Then
resize the card: content should reflow.

## 2. Components and instances
- **Create component:** select, **Ctrl/Cmd+Alt+K**. The original is the **main component**;
  copies are **instances**.
- Edit the main → all instances update. **Overrides** on instances (text, colour, swapped
  icons, hidden layers) persist through updates **as long as the layer names and structure match**.
- Keep main components on a dedicated page (e.g. "Components"), named with slashes for
  grouping: `Button/Primary`, `Input/Text`.
- **Publish** to a team library so other files use them; changes are pushed as library updates
  for others to accept.

## 3. Variants and component properties
- Combine related components into one **component set** with **variants**: e.g. property
  `Type = Primary | Secondary | Ghost`, `State = Default | Hover | Pressed | Disabled | Focus`,
  `Size = S | M | L`. Name layers consistently across variants so overrides survive switching.
- Add **component properties** to cut variant explosion:
  - **Boolean** — show/hide an icon instead of making "with icon"/"without icon" variants.
  - **Instance swap** — choose which icon component sits inside.
  - **Text** — expose label text in the properties panel.
- Design all states (see
  `creative-arts.design-for-form-and-experience.interaction-design.designing-component-states-and-micro-interactions`).
- Use **interactive components** (prototype connections between variants, e.g. hover →
  pressed) so prototypes behave without wiring every screen.

## 4. Variables (tokens) on top
Bind fills, strokes, gaps, padding and radii to **variables** (colour, number, string,
boolean) organised in collections with **modes** (Light/Dark, Compact/Comfortable). Switching
mode on a frame re-themes everything inside. See
`creative-arts.design-for-form-and-experience.design-systems.design-tokens-and-a-modular-type-scale`.

## Gotchas
- **Detach instance** (Ctrl/Cmd+Alt+B) breaks the link forever — updates no longer arrive.
  Avoid; if the component can't do what you need, improve the component.
- **Renaming layers** inside a main component can wipe instance overrides.
- Text set to **fixed width** inside hug containers causes clipping; text usually wants
  "fill" width with auto height.
- Variant explosion (3 types × 5 states × 3 sizes × icon yes/no = 90): use boolean and
  instance-swap properties.
- Groups vs frames: groups have no auto layout or constraints — prefer frames.
- Absolute-positioned children don't affect hug size; badges can overflow.

## Verify
- [ ] Resizing a card or changing a label reflows correctly (hug/fill set intentionally).
- [ ] UI built from instances of main components; nothing detached.
- [ ] Component sets have consistent variant properties and layer names.
- [ ] Booleans/instance swaps used instead of duplicate variants.
- [ ] Colours and spacing bound to variables; mode switch re-themes cleanly.

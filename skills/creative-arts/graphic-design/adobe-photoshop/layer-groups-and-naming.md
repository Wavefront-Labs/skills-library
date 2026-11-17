---
id: creative-arts.graphic-design.adobe-photoshop.layer-groups-and-naming
name: layer-groups-and-naming
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-layers, layer-organisation, layer-groups, layer-naming, colour-coding, layer-filter, artboards, handoff, file-hygiene]
level: practitioner
status: draft
description: "Organise a Photoshop file so anyone can edit it: grouped and named layers, colour labels, filtering, locking and cleanup before handoff to another designer or developer."
sources:
  - https://helpx.adobe.com/photoshop/using/layer-basics.html
  - https://helpx.adobe.com/photoshop/using/selecting-grouping-linking-layers.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Layer groups and naming

**Goal:** a PSD that another designer can open cold and change the headline, swap the
product shot or hide a variant in under a minute.

## Structure
- Top to bottom mirrors front to back: `Type`, `Product`, `Effects/Adjustments`,
  `Background`. One group per visual unit, nested no deeper than 3 levels.
- **Group:** select layers, Ctrl/Cmd+G. **Ungroup:** Ctrl/Cmd+Shift+G.
- Name every layer that matters (double-click the name). Names say role, not content
  ("Headline", "Price badge", "Hero shadow"), so they survive copy changes.
- If you will use **Generate > Image Assets**, layer names ending in `.png`/`.jpg` export
  automatically; keep that in mind before naming.
- **Colour labels** (right-click > colour): e.g. red = do not touch, green = editable copy,
  blue = client-supplied assets. Write the key in a hidden top layer or the handoff note.

## Navigation
- **Layer filter** at the top of the Layers panel: filter by Kind (type, smart object,
  adjustment), Name, Effect, Mode, Attribute or Color label.
- With Move tool, **Ctrl/Cmd+click** on canvas selects the layer under the cursor
  (Auto-Select off avoids accidental moves). Right-click canvas lists all layers there.
- **Alt/Option+click** a group's arrow expands all nested groups.

## Locking and safety
- Lock transparent pixels (paint inside existing pixels only), lock image pixels, lock
  position, lock all. Lock backgrounds and approved logos.
- Group-level **opacity and blend mode** apply to the group as a unit; default group mode
  is Pass Through, which lets inner blend modes affect layers below the group. Set the
  group to Normal to isolate them.

## Cleanup before handoff
- Delete empty layers: File > Scripts > Delete All Empty Layers.
- Delete hidden layers you do not need: Layers panel menu > Delete > Hidden Layers.
- Rasterised type and merged layers are not editable: keep live type and smart objects.
- Package linked smart objects: File > Package (for linked files).

## Gotchas
- Pass Through groups that contain adjustment layers affect everything below the group;
  clip or set the group to Normal if they should not.
- Copying layers between documents with different ppi changes their apparent size.

## Verify
- [ ] Every visible layer has a meaningful name; no "Layer 37 copy 4".
- [ ] Groups collapse to fewer than ~10 top-level items.
- [ ] Hidden or empty junk layers removed; locks set on approved elements.

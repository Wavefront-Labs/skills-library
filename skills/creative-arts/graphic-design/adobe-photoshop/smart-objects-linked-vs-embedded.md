---
id: creative-arts.graphic-design.adobe-photoshop.smart-objects-linked-vs-embedded
name: smart-objects-linked-vs-embedded
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-layers, smart-objects, smart-object-linked, smart-object-embedded, place-linked, relink, package, convert-to-layers, new-smart-object-via-copy]
level: practitioner
status: draft
description: "Choose and manage Photoshop smart objects: embedded vs linked, editing contents, independent copies, relinking, packaging, converting back to layers, and keeping files small."
sources:
  - https://helpx.adobe.com/photoshop/using/create-smart-objects.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smart objects: linked vs embedded

**Goal:** non-destructive, reusable components without bloated or broken files.

## Kinds
| | Embedded | Linked |
|---|---|---|
| Created by | Convert to Smart Object, File > Place Embedded, paste from Illustrator as Smart Object | File > **Place Linked**, CC Library items |
| Content stored | inside the PSD | separate file on disk/cloud |
| Edit | double-click thumbnail opens a .psb/.ai temp | edits the external file; all PSDs using it update |
| File size | grows with each embed | small |
| Risk | none | missing links if the file moves |

## Editing
- Double-click the thumbnail (or Layer > Smart Objects > Edit Contents), edit, **save** and close:
  the parent updates.
- Placed Illustrator art opens in Illustrator - vector stays sharp at any scale.
- Duplicating a smart object layer (Ctrl/Cmd+J) creates an **instance** sharing contents;
  **Layer > Smart Objects > New Smart Object via Copy** makes an independent copy.
- **Replace Contents** swaps the source (e.g. a new screenshot in a device mockup) keeping transforms
  and filters.

## Managing links
- Linked layers show a chain icon; a red ! = missing; a yellow warning = modified (Update Modified Content).
- Layer > Smart Objects > **Relink to File**, **Embed Linked** (make self-contained), **Convert to Linked**
  (export an embedded one to a file to share it).
- **File > Package** collects linked files into a folder with the PSD for handoff.
- **Convert to Layers** (2020+) unpacks a smart object back into its layers in a group.
- Reset Transform restores original size and rotation.

## When not to use
- Painting directly needs a pixel layer (paint on a layer above, clipped).
- Very heavy files nested many levels deep are slow; flatten old nested comps you will not edit.

## Gotchas
- Smart filters apply to the whole smart object; masks on them affect only the filter.
- Embedded camera raw smart objects can be huge; link them instead.
- Sending a PSD with linked smart objects without packaging = broken file for the recipient.

## Verify
- [ ] Links panel/Layers show no missing (red) or modified (yellow) links before delivery.
- [ ] Packaged or embedded for handoff.
- [ ] Shared elements are instances; independent ones made via copy.

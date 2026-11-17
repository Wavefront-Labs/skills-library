---
id: creative-arts.photography-fine-art.adobe-lightroom.ai-masks-subject-sky-background-objects-people
name: ai-masks-subject-sky-background-objects-people
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, ai-mask-types, lightroom-masking, select-subject, select-sky, people-mask, lightroom-classic]
level: practitioner
status: draft
description: "Create AI masks in Lightroom Classic (Subject, Sky, Background, Objects, People, Landscape) and refine edges, update and reuse them across a series."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Masking)", "https://helpx.adobe.com/lightroom-classic/desktop/organize-photos-in-lightroom-classic/smart-collections-criteria-in-lightroom-classic.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AI masks: subject, sky, background, objects, people

Open Masking (`Shift+W`). AI masks compute from image content:
- **Subject** and **Sky**: one click.
- **Background**: inverse of subject with better edge handling.
- **Objects**: brush or draw a rectangle around an item; Lightroom selects it.
- **People**: detects each person; choose whole person or parts (face skin, body skin, eyebrows, eye sclera, iris and pupil, lips, teeth, hair, clothes).
- **Landscape**: separates mountains, water, vegetation, natural ground, architecture, sky, artificial ground.

## Refine
- Add/subtract with Brush (Alt/Option to erase) or intersect with a Luminance Range to keep a sky mask off bright clouds.
- Overlay colour: toggle `O`; Shift+O cycles colours; set overlay to "Image on B/W" to judge edges.
- Feather is not adjustable on AI masks; soften the effect by subtracting a gradient.

## Series workflow
- AI masks recompute on each image when synced or pasted (they are semantic, not pixel copies). Sync a Sky mask with "-0.3 exposure" across a sequence, then check each.
- After a change that alters content (crop, Denoise, Remove), Lightroom flags masks needing update: click **Update** in the Masks panel, or Ctrl/Cmd+click to update all.

## Craft
- Name masks (double-click name): `Sky -0.3 EV`, `Face +0.2`. Essential when revisiting a print file.
- Use subtle values: AI edges show when exposure differences exceed about 0.7 EV.

## Gotchas
- AI masks need Denoise done first for best edges on high-ISO files.
- Hair and fine branches against sky: intersect or subtract a luminance range rather than painting.

## Verify
- [ ] With overlay on at 100%, no halo where the mask edge meets fine detail; toggling the mask shows a natural transition.

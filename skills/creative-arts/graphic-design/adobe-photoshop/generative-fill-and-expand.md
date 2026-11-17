---
id: creative-arts.graphic-design.adobe-photoshop.generative-fill-and-expand
name: generative-fill-and-expand
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, compositing, generative-fill, generative-expand, firefly, content-credentials, photo-manipulation]
level: practitioner
status: draft
description: "Use Photoshop Generative Fill and Generative Expand: selection and prompt strategy, variations, resolution limits, content credentials and commercial-use checks."
sources:
  - https://helpx.adobe.com/photoshop/using/generative-fill.html
  - https://helpx.adobe.com/photoshop/using/generative-expand.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generative Fill and Generative Expand

**Goal:** add, remove or extend image content with Firefly inside Photoshop, keeping it editable and usable.

## Generative Fill
1. Make a selection slightly larger than the area (include some surrounding context).
2. Contextual Task Bar > **Generative Fill**. Empty prompt = remove/fill with surroundings;
   a prompt = add that object ("weathered wooden bench").
3. Result is a **Generative layer** with a mask; Properties shows 3 variations - pick or regenerate.
4. Prompts: describe what to add, not commands ("red umbrella", not "add a red umbrella").

## Generative Expand
- Crop tool, drag the canvas larger, set **Fill: Generative Expand**, Generate. Extends
  background for format adaptations (landscape to portrait, social sizes).

## Resolution and quality
- Generated content is produced at a limited resolution per generation and upscaled to fit the
  selection; very large selections look soft. Work in smaller overlapping selections for big areas.
- Match grain afterwards (add noise over the generative layers) - generated areas are clean.
- Check hands, text, logos, repeating patterns; regenerate or retouch.

## Rights and disclosure
- Content Credentials can be attached on export to record AI use. Check the client's policy on
  generative content; some publishers and stock agencies require disclosure or forbid it.
- Never generate recognisable trademarks or real people for commercial work.
- Generations consume generative credits on the Adobe plan.

## Gotchas
- Requires an internet connection and signed-in account; not available for some account types/regions.
- Generative layers stay editable but add file size; rasterise when final.

## Verify
- [ ] Generated area holds up at 100% at final output size.
- [ ] Usage disclosure decided and recorded with the client.

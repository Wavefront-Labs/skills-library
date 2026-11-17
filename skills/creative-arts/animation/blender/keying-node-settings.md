---
id: creative-arts.animation.blender.keying-node-settings
name: keying-node-settings
category: creative-arts
field: animation
product: blender
tags: [blender, keying, keyer, chroma-key, keying-node-settings, keying-node, despill-factor, green-screen]
level: practitioner
status: docs-checked
description: "Set up the Keying node for green or blue screens: Key Color, Balance, Black and White Level, Edge Size and Tolerance, garbage and core mattes, post blur, dilate, feather, despill."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/keying/keying.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# keying-node-settings

Goal: a clean matte with fine edge detail (hair) from studio green or blue screen footage.

## Node (Keying category > Keying)

The one-stop node for green or blue screen removal: chroma key, despill and common matte tweaks. Inputs: **Image**, **Key Color** (a single colour, or a reference image such as from a Keying Screen node), and the Mask-panel inputs **Garbage Matte** (always excluded) and **Core Matte** (always included).

Settings in working order:
1. **Preprocess > Blur Size**: blurs only the colour (not luminosity) to reduce colour noise; affects the matte calculation, not the result image.
2. **Key > Balance**: balance between colour channels compared with the key colour; 0.5 averages the other two channels (red and blue for green screen). Tweak with the black and white levels while viewing the Matte output.
3. **Tweak > Black Level**: threshold for fully transparent (black in the matte). Keep as low as possible; uneven backdrops need it higher (a Keying Screen helps keep it low). **White Level**: threshold for fully opaque. Keep as high as possible; foreground colours near green may need it lowered. A Core Matte can fix problem areas instead of a low White Level.
4. **Edges > Size** and **Tolerance**: Size is the pixel radius used to detect an edge; Tolerance is the colour difference threshold above which a pixel counts as an edge. Detected edges are not affected by the black and white levels, so fine detail survives. Smaller Size and larger Tolerance give a sharper matte but may lose stray hairs; larger Size and smaller Tolerance capture more detail but can leave a halo.
5. **Postprocess**: **Blur Size** (softens the matte), **Dilate Size** (positive grows, negative shrinks), **Feather Size** (negative inwards, positive outwards) and **Feather Falloff**.
6. **Despill**: **Strength** (0 none, 1 removes all possible spill) and **Balance** (how channels are compared when computing spill).

Outputs: **Image** (matte applied to the alpha channel), **Matte** and **Edges** (view with a Viewer node to adjust Edge Size and Tolerance).

## Workflow

- View the Matte with a Viewer and sample values: screen exactly 0, subject core exactly 1.
- Use a garbage matte for rigs, frame edges and light stands, and a core matte for subject areas with green reflections.

## Gotchas

- Uneven screens: use a Keying Screen node for the Key Color (see keying-screen).
- Edge settings that are too tight make fine hair disappear or flicker.

## Verify

Put the result over a contrasting colour (white, then black) with Alpha Over. No green fringe, no holes in the subject, hair edges preserved.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Keying inputs, Preprocess Blur Size, Key Balance, Black Level and White Level, Edge Size and Tolerance, Mask inputs, Postprocess Blur, Dilate and Feather sizes, Despill Strength and Balance, outputs Image, Matte, Edges. Removed the old Pre Blur 2 to 4 values, the Clip Black/Clip White and Screen Balance names as setting labels, and the two-key tip.
Method: documentation only; no commands were run.

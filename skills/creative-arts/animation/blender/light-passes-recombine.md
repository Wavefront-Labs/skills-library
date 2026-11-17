---
id: creative-arts.animation.blender.light-passes-recombine
name: light-passes-recombine
category: creative-arts
field: animation
product: blender
tags: [blender, render-passes, light-passes, diffuse-pass, glossy-pass, direct-indirect]
level: practitioner
status: docs-checked
description: "Use Cycles and EEVEE light passes: direct, indirect and colour per component, recombining to the combined image in the compositor, and per-pass grading."
sources:
  - https://docs.blender.org/manual/en/latest/render/layers/passes.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/film.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# light-passes-recombine

Goal: split the render into lighting components so each can be adjusted in comp, and recombine to match the beauty.

## Enabling (View Layer Properties > Passes > Light)

Cycles: Diffuse (Direct, Indirect, Color), Glossy (Direct, Indirect, Color), Transmission (Direct, Indirect, Color), Volume (Direct, Indirect), and under Other: Emission, Environment, Ambient Occlusion, Shadow Catcher.
EEVEE (smaller set): Diffuse (Light, Color), Specular (Light, Color), Volume Light, Emission, Environment, Shadow, Ambient Occlusion, Transparent.

Per the manual, the Color passes exclude lighting, and the Direct and Indirect passes exclude the surface colour. That is why light is multiplied by colour when recombining.

## Recombining (Cycles)

```
beauty = (DiffDir + DiffInd) * DiffCol
       + (GlossDir + GlossInd) * GlossCol
       + (TransDir + TransInd) * TransCol
       + VolumeDir + VolumeInd + Emission + Environment
```
Use Mix Color nodes (Add and Multiply) or Math nodes in the compositor, and group the result as a "Recombine" node group to reuse it. The formula follows from the pass definitions; confirm it against Combined on your own scene (see Verify) because the manual does not print it.

## Grading per pass

- Brighten only bounce: scale DiffInd before the multiply.
- Tint the specular: colour-correct GlossDir plus GlossInd.
- Lighten shadows without changing highlights: adjust Indirect, not Direct.

## Gotchas

- When Film > Transparent is on, the world is excluded from the final render. The manual says the Environment pass can then be used to get the environment colour and composite it back in.
- Denoising: denoise light passes separately (see denoising-data-passes) or compare against an un-denoised Combined.
- Holdout materials and shadow catchers change what goes into each pass, so check edge cases.
- Extra passes cost memory and render time.

## Verify

Recombine in the compositor and Difference-blend against the Combined pass with denoising off. The result should be near black apart from noise. Any visible residue points to a missing pass (for example Environment, Emission or a Volume pass).

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST).
Confirmed: Cycles and EEVEE light pass names and definitions; Color passes exclude light; Environment pass purpose when Film Transparent is on.
Removed as unconfirmed: the claim that the Environment pass is empty with Film Transparent (the manual says the opposite), the "12 extra float buffers" figure, and the claim that denoising is applied to Combined only.
Method: documentation only; no commands were run.

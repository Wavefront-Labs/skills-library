---
id: creative-arts.animation.blender.cloth-garment-modeling
name: cloth-garment-modeling
category: creative-arts
field: animation
product: blender
tags: [blender, cloth, garment, clothing, costume, edge-loops, folds, solidify, thickness, deform, weight-paint, cel, toon, outline, rigging, modeling]
level: advanced
status: docs-checked
description: "Model stylized garments in Blender that read flat for cel, deform cleanly on a rig, and outline safely — edge loops at folds, Solidify thickness, built to deform."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/solidify.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/smooth_by_angle.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/mirror.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cloth-garment-modeling

Goal: model garments that read as clean stylized shapes under a 3-tone cel ramp, deform predictably when the character moves, and take the inverted-hull outline without artifacts. This is **modeled** cloth — built and hand-sculpted to look and deform right — not cloth simulation (dynamics are a separate skill). It ties to costume design intent on the front end and to `creative-arts.animation.blender.rigging` on the back end; shading is owned by `creative-arts.animation.blender.cel-shading`, and garments with placed graphics also touch `creative-arts.animation.blender.uv-unwrapping`.

## Modeled vs simulated — why modeled for cel

Cloth simulation produces thousands of tiny, noisy, frame-varying wrinkles. Under Shader-to-RGB + CONSTANT 3-tone ramp those wrinkles become **crawling tone bands**, and under the inverted-hull outline they become **flickering black scribbles** that change every frame — death to a clean cel look and impossible to keep consistent on a reused locked asset. So cel garments are **modeled as deliberate, chunky folds** that stay put and read as shapes, exactly like the hair groom. You sculpt the folds you want; you don't let physics invent them. Reach for sim only in the rare shot that needs it, then bake it.

## Build the garment to deform, not to drape

A garment is skinned to the same armature as the body, so model it the way the body is modeled: **as a deform-ready surface following the character's forms**, offset outward.

- Start from the body mesh where possible: duplicate the torso/limb faces the garment covers, `Shrinkwrap` or just push them out slightly, and build from that so the garment shares the body's edge flow and sits flush.
- Keep it **all quads with even spacing** across areas that bend — the same rule as `character-modeling`. A sleeve full of triangles kinks and pinches when the elbow bends.
- Model in a **neutral/A-pose** matching the body's bind pose, with the deliberate folds already sculpted in. Not a drape — a *design*.

## Edge loops at folds and deform zones

This is the heart of it. Folds and joints need loop density, or they crease wrong:

- Put **2–3 supporting edge loops at every major fold** you want (elbow pit, knee, waist gather, shoulder, armpit, where a jacket breaks at the hip). The loops hold the fold's shape and give the surface somewhere to compress into when the joint bends, instead of collapsing into a pinch.
- Run **continuous loops around limbs and torso** (like body topology) so a bend distributes across several loops, not one. A single loop at an elbow folds like cardboard; three loops fold like cloth.
- Model the **primary stylized folds as actual geometry** — a few bold diagonal folds down a sleeve, a gather at a cuff, the hang of a coat hem. Reinforce each with supporting loops so it survives subsurf and deform.
- Keep fold geometry **readable at delivery res** — chunky folds the 3-tone ramp can band and the outline can catch, not micro-wrinkles.

Loop placement mirrors joints: wherever the rig bends (ties to `creative-arts.animation.blender.rigging`), the garment needs the same loop support the skin has.

## Thickness via Solidify

Garments are surfaces; cloth has thickness, and the outline needs a solid to wrap:

- Add a `Solidify` modifier. **Offset** runs from -1 to 1 and places the solid inside or outside the original surface, decided by the face normals; 0.0 centres it on the original mesh. Keep **Thickness** small and scale-appropriate. Thickness uses local coordinates, so apply or clear non-uniform object scale first.
- Solidify gives the garment a real edge at the hem, cuff and collar — so the outline draws a crisp line at the garment's border instead of outlining a zero-thickness sheet (which flickers and punches through, same failure as hair cards).
- Keep Solidify **non-destructive** in the stack: `Armature` deform first (or let Solidify sit above/below per need — generally Solidify *after* subsurf so the shell is even), `Smooth by Angle` last.
- Keep **Rim > Fill** on so the hem/cuff has capped geometry the outline and ramp can read.

## Modifier stack for a garment

Typical, top to bottom:

1. `Mirror` (if symmetric), with **Clipping** and **Merge** on.
2. `Subdivision Surface` — only if the garment is built in a clean quad cage and carries no booleans.
3. `Solidify` — thickness, Rim Fill on.
4. `Smooth by Angle` modifier (Angle sets the maximum angle between face normals treated as smooth; added by the Shade Auto Smooth operator) — last, so it reads final geometry.
5. `Armature` — usually the *deform* driver; in practice the Armature modifier is placed so the garment deforms with the body (commonly above Subsurf so you subdivide the deformed cage, or below depending on taste — pick one and keep it consistent across the series).

Avoid booleans on garments entirely — use modelled holes (buttonholes, pockets) with clean loops, for the same subsurf-boolean reasons as `hard-surface-modeling`.

## Weighting to deform cleanly

- Skin the garment to the **same deform bones** as the body underneath. Easiest reliable method: transfer the body's weights to the garment (for example with the Data Transfer modifier, see `data-transfer-modifier`), so the garment inherits the body's clean weights, then clean up seams and hems by hand.
- **Hems, cuffs and collars** often want slightly different weights than the skin so they move as an edge (a coat hem shouldn't shrink-wrap the leg). Hand-paint those zones.
- Check for **interpenetration**: the garment must stay outside the body through the full range of motion. Add a thin gap in the bind, and where it still pokes through, either repaint weights or add a corrective shape key (ties to `creative-arts.animation.blender.facial-rig`/blendshape workflow for the corrective-shape technique).

## Keeping it cel-outline-safe

- **Solidify thickness ≥ outline offset**, or the outline punches through the cloth edge.
- **Consistent normals** (Recalculate Normals Outside) across the whole garment; a flipped face = black outline blob.
- **Weld seams** (`Merge by Distance`) so the shell is watertight; `Delete Loose` so no stray edges spawn floating outline fragments.
- `Mark Sharp` the deliberate hard garment edges (collar fold, lapel, belt line) so the outline catches them; leave soft folds unmarked so the outline stays on the silhouette and the big folds.
- Keep **fold geometry bold** so each fold reads as one clean band and one clean line — micro-folds alias and crawl.

## Pose-driven corrective folds

Modeled folds look static if they never change through a motion, and the big ones *should* shift when a joint bends. Borrow the corrective-shape technique from `creative-arts.animation.blender.blendshape-sculpting`:

- Sculpt a **shape key per major joint pose** that deepens/moves the fold the way cloth would — e.g. `cor_elbow_bend` that pushes the inner-elbow fold in as the arm closes, `cor_hip_sit` that bunches the lap of a coat.
- Drive each key with a **Driver reading the bone rotation** (right-click the key's Value > Add Driver, variable = the joint bone's rotation, expression ramps 0→1 across the bend).
- This gives hand-authored, deterministic "cloth motion" with zero simulation — the folds move the same in every shot (locked reused asset) and never crawl under the cel ramp.
- Keep these few and bold — one or two per major joint. They are acting, not physics.

## Collars, cuffs, hems and layered garments

Garment edges are where cel reads cleanly or falls apart:

- Model a **collar/lapel as its own thickened piece** with `Mark Sharp` on the fold, so the outline draws a decisive line and the ramp bands the inner vs outer face distinctly.
- **Cuffs and waistbands** get their own loops and slightly stiffer weights so they hold shape instead of shrink-wrapping — a cuff should read as a ring, not paint on the wrist.
- **Layered garments** (shirt under open jacket): keep each layer a separate object with a real gap between them so the outline draws the jacket edge over the shirt. Weight the under-layer so it never pokes through the over-layer at any pose.
- Give **hems real thickness and a touch of modelled wave** so a coat bottom reads as cloth, and mark the hem edge Sharp for the outline.

## Flat/stylized read under the ramp

- Model **broad, flat planes** between folds — the ramp bands these cleanly. Scatter of small bumps = scatter of noisy tone.
- Use **separate materials** per garment part (shirt vs trim vs buttons) so the cel shader fills them with distinct flat colours and the outline draws between them.
- Decals/graphics (a logo, a patch) go through `uv-unwrapping` — unwrap just that panel, leave the flat-fill body un-unwrapped.

## Verify

A cel garment is finished when:

1. **Deform test:** pose the rig through extremes (arms fully up and crossed, deep crouch, full spine twist) — the garment follows the body, folds compress into their supporting loops instead of pinching, and **no part of the body pokes through** at any pose.
2. **Fold read:** a 3-tone EEVEE render shows the big folds banding as stable, readable shapes that **don't crawl** as the character moves (crawling = too-fine folds or a sim left in — re-model chunkier).
3. **Outline test:** inverted-hull outline on — clean continuous line on the garment silhouette, hem, cuff and collar, lines between garment-part materials, no black blobs (flipped normals) and no line punching through the cloth edge (Solidify too thin).
4. **Watertight:** Merge by Distance removes nothing and a non-manifold selection finds nothing (apart from deliberate open hems).
5. **Topology:** areas over joints are continuous quads with ≥2 supporting loops at each major fold; no n-gons remain under any subsurf.
6. **Consistency:** the garment deforms identically when the same rig pose is loaded in a different shot file (locked reused asset behaves deterministically — no sim drift).

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: Solidify Offset range and normal-based inside/outside rule, thickness uses local coordinates, Rim Fill option, Smooth by Angle modifier name and its Angle option, Mirror Clipping and Merge options. Corrected: the modifier is Smooth by Angle (not Shade Auto Smooth) and the EEVEE name; removed typical thickness values, Subdivision levels and menu paths for weight transfer and selection tools that were not confirmed.
Method: documentation only; no commands were run.

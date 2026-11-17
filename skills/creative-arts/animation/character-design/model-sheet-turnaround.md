---
id: creative-arts.animation.character-design.model-sheet-turnaround
name: model-sheet-turnaround
category: creative-arts
field: animation
product: character-design
tags: [model-sheet, turnaround, orthographic, front-side-back-three-quarter, expression-row, viseme-row, mouth-chart, color-callout, hex, proportion-grid, height-chart, on-model, consistency, blender-ortho, turntable, reference, turnaround-alignment, color-model, character-orthographics]
level: advanced
status: draft
description: "Build the canonical turnaround/model-sheet every shot is checked against, and shoot a Blender ortho turntable to prove a built model is on-model."
sources:
  - "Preston Blair, Cartoon Animation (model sheets, construction)"
  - "Tom Bancroft, Creating Characters with Personality (turnaround discipline)"
  - "Standard animation-production model-sheet practice"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# SKILL: Model-sheet / turnaround production (expert)

Produce the **canonical reference artifact** that turns a locked design
(`character-design-craft`) into something a modeller builds from, a rigger rigs to, an
animator stays on-model against, and a reviewer checks every shot against. Then **prove**
the built model matches it by shooting an orthographic turntable in Blender. This is the
contract: if it's not on the sheet, it's not canon; if the model doesn't match the sheet,
the model is wrong. Pairs with `character-design-craft`, `expression-design`,
`creative-arts.animation.blender.character-blockout`, and
`creative-arts.animation.blender.character-modeling`.

A pretty concept painting is not a model sheet. A model sheet is a *measurement document*.

---

## 1. What a complete character pack contains

1. **Orthographic turnaround** — minimum **front / side / back**; add **3/4 (front-three-
   quarter)** for any form a modeller can't infer from F+S+B (most hero characters).
   Same character, same height, same scale, features on the same horizontal lines across
   every view (§2).
2. **Proportion grid / height chart** — horizontal guide-lines in head-heights through
   top-of-head, eye-line, chin, shoulder, elbow, waist, wrist, crotch, knee, ankle. Every
   view snaps to these. This is the spine of the whole sheet (§3).
3. **Expression row** — the locked set from `expression-design` (6 basics + show extras),
   labelled, drawn on this character.
4. **Mouth chart / viseme row** — the 9 Rhubarb visemes `A B C D E F G H X` for lip-sync
   (`creative-arts.animation.blender.lip-sync`), shown as mouth shapes.
5. **Hands & feet** — relaxed, fist, point, open; and the foot from the needed angles.
   Hands are where models fall apart; give them their own detail cells.
6. **Props / costume callouts** — any detachable or signature prop, with its own small
   turnaround and attach-point note.
7. **Colour callout** — flat colour chips with the **locked hex** labelled per part
   (base / shadow / accent / emissive), copied from the design lock. Include the cel
   *shadow* hue, not just base (`creative-arts.animation.blender.cel-shading` hue-shifts
   shadow) (§4).
8. **Construction notes** — dominant shape, the one deliberate asymmetry, loop/deformation
   intent, do/don't list ("antennae never droop except the 1-frame crack").
9. **Scale comparison** — the whole cast lined up at correct *relative* heights.

---

## 2. Orthographic rules (break these and the model is born broken)

- **TRUE orthographic — zero perspective.** Front and side are the same character at the
  same scale with every feature at the same height. The modeller loads these as background
  images and traces them; any foreshortening bakes a permanent error into the mesh. Shoot/
  draw with a parallel (ortho) projection, never a perspective lens.
- **Front and side MUST share heights.** Eye-line, chin, shoulder, waist, knee — identical
  Y on both views. This is the single thing that makes F+S background images produce a
  correct 3D form. Enforce it with the proportion grid (§3), not by eye.
- **Neutral pose = relaxed A-pose**, arms ~45° down, clear of the torso. Not T-pose:
  T-pose shoulders model and weight badly (the deltoid skin stretches wrong), and A-pose
  matches the mocap intake pose (`creative-arts.animation.blender.mocap-retarget`). Limbs
  must not overlap the body in any view, or there's nothing clean to trace.
- **Closed, consistent line weight.** One outline weight for the form; interior
  construction lines on a separate, hideable layer. Open or broken outlines read as holes
  and confuse the trace.
- **Symmetric where the design is symmetric;** draw the one deliberate asymmetry
  (`character-design-craft` §7) explicitly and label it so the modeller doesn't "correct"
  it back to symmetric.

---

## 3. The proportion grid (the measuring system)

- Set the character's **head-height as the unit** (from `character-design-craft` §4) and
  rule horizontal lines at each anatomical landmark in head fractions. Label them.
- Every view hangs off these lines. The eye-line on the front view is the eye-line on the
  side and 3/4 — same pixel row.
- **Pin a known real-world scale** so the sheet imports to true size: decide "character is
  N head-heights = M metres", so the modeller/`character-blockout` sets the Blender scale
  and the half-extent maths lands right (that skill's §scale-law depends on a trustworthy
  reference size).
- The cast scale-comparison (§1.9) reuses this: all characters on one shared height ruler.

---

## 4. Colour callout (lock the hex, include the shadow)

- Flat chips, one per part, labelled with **exact hex** from the design lock — base colour
  *and* the cel shadow colour (the ramp's dark band is a hue-shifted colour, usually toward
  blue, not just a darker base; `cel-shading` does this in the ColorRamp). Give both or the
  look-dev re-invents the shadow and it drifts.
- Mark **emissive** parts (Chip's mint screen, any HUD/LIVE dot) and their strength intent —
  they get no outline and plain Emission (`character-blockout` §emissive).
- Note **material intent** per part: matte / glossy / emissive. Keep the palette to the
  design's 3–5 locked colours; the accent is the eye-anchor.

---

## 5. Producing the sheet (process)

1. Lay a single canvas with the **proportion grid** first — horizontal landmark rules in
   head units.
2. Draw **front** on the grid, then **side** and **back** snapping every landmark to the
   same rules; add **3/4** last (it won't line up on horizontals the same way — use it as a
   form-clarifier, not a trace source).
3. Keep the form outline on one layer, construction on a hideable layer.
4. Add the **expression row**, **viseme row**, **hands/feet**, **props**, **colour callout**,
   **construction notes**, **cast scale comparison**.
5. **Export per-view PNGs at a known pixels-per-unit** (so proportions import to real
   scale): `front.png`, `side.png`, `back.png`, `34.png` — one file per ortho view, same
   pixel-height, transparent background.
6. Lock the whole pack as canon beside the character's `.blend` (locked-asset discipline);
   this is now the source of truth every shot is checked against.

---

## 6. Blender handoff — background images for modelling

- Add **Reference / Background Images** (Empties set to *Image*) in Front (Numpad 1) and
  Side (Numpad 3) *orthographic* views; load `front.png` / `side.png`; set each empty's
  axis to the matching view and lock it. Model to the silhouette.
- Match the import scale to the grid's pixels-per-unit (§5.5) so the mesh comes out at true
  size. Verify by checking a known landmark height against the grid.
- See `creative-arts.animation.blender.character-modeling` /
  `creative-arts.animation.blender.sculpt-retopo` for the build itself.

---

## 7. Shoot a turntable to PROVE the model is on-model

The reverse direction, and the step most pipelines skip: once the model is built, render an
orthographic turntable and **overlay it on the sheet**. This is how you catch drift before
it reaches a shot. Headless-scriptable (`creative-arts.animation.blender.character-blockout`
already does exactly this for the blockout — reuse that builder's turntable code):

1. Camera `data.type = 'ORTHO'`; tune `ortho_scale` to frame the character's height; set
   `scene.render.film_transparent = True` for clean alpha.
2. Parent all parts to an **Empty at origin**; rotate the Empty (not the camera):
   `pivot.rotation_euler = (0, 0, radians(deg))`, then `view_layer.update()`, render at
   `deg ∈ {0, 90, 180, 270}` (front/side/back/other-side) — and 45 for the 3/4.
3. Render each at the **same pixel-height as the sheet exports** so they overlay 1:1.
4. **Overlay render-on-sheet** (`magick composite -blend 50 render_front.png
   sheet_front.png check_front.png`, or difference-blend). Landmarks must land on the grid
   lines; silhouette must match within line-weight tolerance.
5. For a fuller check, spin 24–36 frames into a turntable mp4
   (`creative-arts.animation.blender.rendering-amd-hip` for render settings) and eyeball
   that the silhouette stays on-model through the full rotation — 3/4 angles expose errors
   front+side hide.

A model that fails the overlay goes back to the modeller; the sheet wins, always.

---

## Verify

A reviewer passes a pack only when all hold:

- [ ] **Front / side / back present** (+ 3/4 if the form needs it), same character, same
      scale.
- [ ] **True orthographic** — no perspective/foreshortening in any view (parallel
      projection).
- [ ] **Heights match across views** — eye-line/chin/shoulder/waist/knee identical Y on
      front and side (checked against the grid, not by eye).
- [ ] **Proportion grid** in head-units present and labelled; real-world scale pinned (§3).
- [ ] **A-pose**, limbs clear of body, closed consistent outline, construction on a hideable
      layer.
- [ ] **Expression row** (the `expression-design` set) + **9-viseme mouth chart** present,
      drawn on this character.
- [ ] **Hands/feet** detail cells + **prop** callouts present.
- [ ] **Colour callout** = locked hex per part including the **cel shadow** colour and
      emissive marks; palette ≤5 colours; accent noted.
- [ ] **Construction notes:** dominant shape, the one asymmetry (labelled so it isn't
      "fixed"), loop/deformation intent, do/don't list.
- [ ] **Cast scale comparison** on a shared height ruler.
- [ ] **Per-view PNGs exported** at a known pixels-per-unit, matched height, transparent.
- [ ] Pack **locked beside the `.blend`** as canon.

**Runnable check (on-model proof, the whole point):** render the built model's ortho front
and side at the sheet's pixel-height (§7), then
`magick compare -metric AE -fuzz 8% render_front.png sheet_front.png diff_front.png`
(difference-overlay also fine for a human). The silhouette and every grid landmark must
land within line-weight tolerance; a model whose landmarks miss the grid lines is
off-model and fails — send it back to the modeller. Re-run after any model change.

---

## Pitfalls

- **Perspective reference** → unmodelable; the mesh inherits the foreshortening forever.
- **Front/side heights not matching** → background-image trace produces broken proportions.
- **T-pose** → bad shoulder deformation + mismatch with the mocap intake pose; use A-pose.
- **Open/overlapping outlines** → the trace reads holes; limbs tucked against the body give
  nothing clean to trace.
- **Hex not locked (or shadow colour missing)** → colour drifts shot to shot; look-dev
  re-invents the shadow.
- **No turntable proof** → the model silently drifts off the sheet and nobody notices until
  a shot looks wrong (§7 is the guard).
- **3/4 treated as a trace source** → it won't share horizontals cleanly; use it to clarify
  form, trace from front+side.
- **Concept painting masquerading as a model sheet** → no measurements, nothing to check
  against; it's reference, not canon.

Pack order: design in `character-design-craft` → acting in `expression-design` → lock here →
build in `creative-arts.animation.blender.character-blockout` / `character-modeling` → shoot
the turntable (§7) → every shot checked against this sheet forever.

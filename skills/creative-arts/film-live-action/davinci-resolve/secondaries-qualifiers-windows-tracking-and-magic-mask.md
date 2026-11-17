---
id: creative-arts.film-live-action.davinci-resolve.secondaries-qualifiers-windows-tracking-and-magic-mask
name: secondaries-qualifiers-windows-tracking-and-magic-mask
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, colorist, colourist, color-page, secondary-correction, secondaries, qualifiers, qualifier, hsl-qualifier, luma-qualifier, 3d-qualifier, key, matte-finesse, power-windows, windows, circle-window, polygon-window, gradient-window, window-tracking, tracker, cloud-tracker, point-tracker, 3d-tracking, feature-tracker, magic-mask, person-mask, object-mask, face-refinement, key-mixer, outside-node, highlight-view, matte-view, skin-tone-isolation, sky-isolation, vignette, relight, depth-map, object-removal, keyframes-colour, dynamics, qualifier-refinement, matte-finesse-use, 3d-qualifier-use, window-shapes, window-feather, window-combining, tracker-detail, interactive-tracking, magic-mask-person, magic-mask-object, magic-mask-strokes, key-mixer-use, combining-mattes, matte-math, face-refinement-use]
level: practitioner
status: draft
description: "Isolate and grade parts of the frame in Resolve: HSL/luma/3D qualifiers with matte finesse, Power Windows with tracking, Magic Mask, Face Refinement, key mixing and outside nodes, keyframed dynamics."
sources:
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (The Colorist Guide to DaVinci Resolve - Secondary corrections, Windows, Tracking, Magic Mask chapters)"
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Color page - Qualifier, Window, Tracker, Magic Mask)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secondaries: qualifiers, windows, tracking and Magic Mask

**Goal:** change one thing in the frame - a face, a sky, a lamp, a distracting red -
without the audience seeing an edge, a flicker or a crawl. Secondaries are always on
their own node after the balanced primary.

## 1. Qualifiers (colour keys)
Add a new serial node (`Alt+S`), open the **Qualifier** palette:
- **HSL**: pick with the eyedropper (drag over the colour), add with `+` picker, subtract
  with `-`. Tune Hue/Saturation/Luminance ranges and *softness* per band. Toggle a
  band off when it isn't helping (e.g. luminance for skin keys).
- **Luma**: for sky/highlights/shadows only.
- **3D**: draw strokes on the viewer; the keyer builds a 3D colour-space key - faster and
  cleaner for skin and complex colours.
- **RGB**: per-channel ranges for specific colours.
View the matte with the **Highlight** button (`Shift+H`; the A/B toggle shows grey
vs black-and-white matte). Then **Matte Finesse**: *Clean Black* / *Clean White* to
fill holes, *Blur Radius* and *In/Out Ratio* for edges, *Denoise* on noisy keys,
*Pre-Filter*, *Shrink/Grow*. The key should be slightly soft; hard keys chatter.
Combine with a window (intersect) to stop the key grabbing the same colour elsewhere.

## 2. Power Windows
**Window** palette: Linear/Rectangle, Circle, Polygon, Curve (B-spline), Gradient.
Draw in the viewer; *Softness* (inside/outside) feathers; *Invert* for vignettes; multiple
windows per node combine with the **Mask** toggle (add/subtract per window).
Uses: vignette (circle window, inverted, lower gain), relight a face (soft circle, +offset),
darken a wall, gradient for a sky. Keep windows **large and soft** - an audience
sees a tight window moving before it sees the grade.

## 3. Tracking
**Tracker** palette with a window selected:
- **Cloud tracker** (default): analyses feature points in the window; track *Forward*
  from the first frame (`Alt+Shift+T` interactive). Enable Pan/Tilt/Zoom/Rotate/
  Perspective 3D as needed; turn off the ones the shot doesn't do to prevent drift.
- **Point tracker**: place points on specific features when the cloud grabs the
  wrong thing (a moving person behind the window).
- **Interactive mode**: delete/add feature points inside the window before tracking.
- When the subject is occluded or leaves frame: track to the problem, then use
  **Frame** mode to keyframe the window by hand for the gap (*Clip* vs *Frame* in the
  tracker). Reset tracking from a reference frame if it drifts.
- Tracking data copies to other windows on the node via *Copy/Paste Track Data*.
- **Stabilize** mode in the same palette for smoothing camera shake (Perspective,
  Similarity, Translation; *Camera Lock* for a locked-off look).

## 4. Magic Mask (AI)
**Magic Mask** palette: *Person* (whole body or features: face, hair, skin, clothes,
arms...) or *Object*. Draw a short stroke on the subject, press *Track Forward*; mask
appears as the node's key. Refine with `+`/`-` strokes on frames where it fails,
*Quality: Better* for finer edges, *Mask Refinement* (shrink/grow, blur, cleanup).
Combine with a qualifier (skin) by intersecting keys. Resolve 19 adds improved
segmentation and object masks; check edges on hair and motion blur before trusting it.
**Face Refinement** (OpenFX > Resolve FX Refine > Face Refinement) auto-tracks faces
and offers skin smoothing, eye/lip/cheek adjustments - use the sliders gently.

## 5. Combining keys: Key Mixer and outside nodes
- **Outside node** (`Alt+O`): new node receiving the *inverse* of the previous node's key -
  grade the subject on one node and the background on the next with one key.
- **Key Mixer** (Node Editor > Add Key Mixer): combine several nodes' keys (add,
  subtract, intersect) into one matte feeding a grade node; also the way to reuse a
  key from an earlier node (link the key output, blue triangle, into the mixer).
- **Key** palette per node: *Key Input* gain/offset, *Invert*, *Mask/Matte* mode and
  the output key gain to blend a grade partially.

## 6. Dynamics (keyframing)
Keyframe palette (right of the node graph): *Dynamic* keyframes interpolate (a grade that
changes as a window moves through light), *Static* hold. Mark keyframes with
`Ctrl/Cmd+[` / `]`; *Dynamic* attribute ease via right-click. Keep keyframed grades on
their own node so static grades stay simple.

## Gotchas
- Hard-edged keys that chatter frame to frame: add blur radius and denoise, or use a 3D key.
- Windows tracked with rotation enabled on a locked-off shot; the window wobbles.
- Magic Mask on a wide shot with many people; it jumps between them - add a window.
- Skin isolation without a window; the wooden table gets "skin" too.
- Secondaries built on the balance node; one change to the balance breaks every key.

## Verify
- [ ] Each secondary on its own node, labelled, after the balance node.
- [ ] Mattes viewed in Highlight mode; edges soft; no chatter when played at speed.
- [ ] Tracks checked through the whole clip; occlusions keyframed.
- [ ] Combined keys use Key Mixer/outside nodes rather than duplicated qualifiers.

---
id: creative-arts.animation.blender.character-modeling
name: character-modeling
category: creative-arts
field: animation
product: blender
tags: [blender, modeling, topology, edge-flow, quads, poles, subsurf, retopo, cel, outline, stylized, character, rig-ready, murder-drones]
level: advanced
status: verified
description: "Build appealing, clean-quad, riggable, cel-correct stylized characters in Blender: edge flow, loop budgets, pole management, subsurf, outline-safe scale."
sources: []
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# Character Modeling for a cel-shaded series (Blender)

**Goal:** turn "primitive blobs" into appealing, on-model, *riggable*, *cel-correct*
characters that read in close-up and as a flat black silhouette, deform without
pinching, subdivide without falling apart, and carry a consistent ink line every
shot. Model once, apply transforms, lock the `.blend`, reuse forever.

The current cast is blockout-tier: a `uv_sphere` body, a `cube` head, `cylinder`
rubber-hose arms, no face. That is a proportion study, not a model. Everything
below is how a modeler with decades in feature + stylized series actually fixes it.

---

## 0. Why "blob" fails, concretely

A joined pile of primitives fails for four independent reasons, and you must fix
all four or the character stays blockout-tier:

1. **No edge flow.** A `uv_sphere` has pole-fan topology at top/bottom and evenly
   spaced rings everywhere else. Loops run with the sphere, not with the *form*
   (no brow, no eye socket, no mouth bag). It can never hold an expression.
2. **No deform loops where joints bend.** A `cylinder` arm has rings along its
   length but none *concentrated* at the elbow. Bend it and the silhouette
   collapses to a crease or balloons — there is nothing for the rig to rotate
   around cleanly.
3. **Disjoint islands.** Sphere + cube + cylinders *intersecting* but not welded
   is not one surface. Subsurf treats each island separately: each shrinks toward
   its own centroid (Catmull-Clark pulls a closed island ~inward by up to a
   quarter of its edge length at the boundary), so arms visibly *detach* from the
   body and the head floats off the neck. **This is the project's recurring bug.**
   See §6.
4. **Scale is unfixed.** Outline thickness here is a world-unit Solidify shell
   (see `cel-shading.md`). If one character is 1.7 units tall and another is 60,
   their ink lines differ by 35x. Blobs built at random primitive sizes guarantee
   inconsistent line weight.

---

## 1. Box-model vs sculpt+retopo — pick per character

- **Box / poly-model (default for this show).** Start from a cube, extrude and
  loop-cut to the forms, build topology *correctly the first time*. Right for
  hard-surface and simple stylized heads (Pixel's CRT case, Moss, most props).
  Fast, and the topology is clean by construction — no retopo pass.
- **Sculpt → retopo.** Only when the form is organic and hard to reason about as
  a cage (Nana Wren's lived-in face, a creature). Block a Multiresolution or Dyntopo
  sculpt for the *shape*, then lay new quad topology over it with the Poly Build
  tool / `Shrinkwrap` (target = sculpt, `Project` mode, with `Snap to Face`). The
  sculpt is a reference surface you throw away; the retopo cage is the deliverable.

For a cel show that is mostly flat forms, **box-model 80% of the cast.** Sculpt is
expensive and the toon ramp hides the micro-surface sculpt gives you. Reach for it
only when you genuinely cannot see the topology in your head.

---

## 2. How much geometry cel actually needs

Cel shading quantizes lighting into 2–3 bands; it does **not** reward dense
surface detail — a high-poly nose and a crisp low-poly nose read identically once
banded. So the budget rule is **crisp forms over density, but enough loops to
deform.**

Working stylized-TV budgets (quads, pre-subsurf control cage):

- Head: ~800–1,500 faces. Enough for eye loops, mouth loops, brow, ear stub.
- Full body (clothed, simple): ~2,500–5,000 faces.
- Hero face in close-up: push head to ~2,000 for extra mouth-corner and lid loops.

If you are past ~8k on a simple stylized character you are modeling detail the
ramp will flatten — stop and ask what loop is actually doing deform or silhouette
work. **Every loop must earn its place by doing one of: silhouette, deform, or a
sharp shading/outline break.** Delete the rest.

---

## 3. Edge flow — loops follow the form

The single difference between blob and appeal. Edge loops must trace the muscle /
form lines of the face so that when the rig or shape keys push them, the surface
slides along believable lines instead of tearing.

**Concentric loop islands (the non-negotiable facial structure):**

- **Eyes:** a ring of **3–4 concentric loops** encircling each eye socket, like
  tree rings. The innermost loop is the lid edge (hugs the eyeball); the outer
  ones give the brow-above / cheek-below bulge room to move. These loops must form
  a clean closed ring — never terminate a loop *inside* the eye ring, or the lid
  pinches when it blinks.
- **Mouth:** a ring of **3–4 concentric loops** around the lips forming a **mouth
  bag** — the tube of geometry that lets the mouth open, pucker, and smile. The
  innermost loop is the lip edge; outer loops are the nasolabial / chin-crease
  region. Critically, the **mouth corners** get an extra pole-free junction so a
  smile can pull the corner back without collapsing (this is where blobs always
  tear).
- **Brow ridge:** 2 horizontal loops crossing the forehead above the eye rings so
  the brow can furrow and raise as a distinct form — the current cube head has no
  brow, so the face reads dead.
- **Nose / cheek:** loops from the nose wing sweep into the eye ring and the mouth
  ring (the classic "loop around eyes + loop around mouth, joined at the nose and
  temple" layout). This is the face loop topology every feature studio uses;
  replicate it even stylized.

**Body deform loops:** concentrate **2–3 loops** exactly at each bending joint —
elbow, knee, knuckle, jaw hinge, waist. One loop *at* the pivot, one just above,
one just below, so the bend has volume to rotate through. A single ring (blob
cylinder) folds flat; three rings keep the cross-section round through a 90-120°
bend. Keep loops evenly spaced around joints (even quads) for predictable weight
painting.

---

## 4. Pole management

A **pole** is a vertex where not-four edges meet: **5-pole** (E-pole, 5 edges) and
**3-pole** (N-pole, 3 edges) are the only two you use. Poles are how you redirect
or terminate edge flow — you *need* them, but they shade and deform badly, so
place them deliberately.

Rules, in priority order:

1. **Never put a pole on a deforming crease** (eyelid edge, lip edge, elbow pivot).
   It will pinch visibly when animated.
2. **Never put a pole where it catches a highlight/terminator** on a flat visible
   area (cheek, forehead center). On a banded cel surface a pole can snag the tone
   boundary and make a dimple-shaped shadow artifact.
3. **Good homes for poles:** the corner of the mouth bag, the top of the nose wing,
   the back of the skull / inside the ear, the crotch/armpit junction, under the
   jaw — hidden, low-deform, low-visibility spots.
4. **Use a 5-pole to spread a loop into a fan** (e.g., to add cheek loops without
   carrying them all the way around the head) and a **3-pole to kill a loop** you
   no longer need. The eye and mouth rings each typically resolve into the
   surrounding mesh via one 5-pole at the outer temple/cheek corner — that is the
   correct, standard location.

A quad-dominant mesh with a handful of poles in hidden spots is the target. If you
have *zero* poles you are probably carrying loops you don't need all the way
around the head (wasteful) or you built a pure grid that can't follow the form.

---

## 5. Subdivision strategy — and the detachment bug

Decide **before** modeling whether a character ships subdivided:

- **Subsurf on (organic/soft characters).** Model a low control cage (§2 budgets
  are *cage* counts), add a `Subdivision Surface` modifier (level 1 viewport / 2
  render typically — stylized rarely needs 3). Control sharpness with **edge
  creases** (`Shift+E`, crease weight 0.8–1.0 for a near-hard edge) or, cleaner,
  with **supporting loops** (a loop pair tight either side of an edge holds it
  crisp). Creases are faster to author; support loops give more predictable cel
  outline behavior. Prefer support loops on anything the inverted-hull outline
  touches.
- **Subsurf off (hard-surface / sharp characters).** Model the final resolution
  directly, use `Shade Flat` + Auto Smooth (Blender 4.x: the "Smooth by Angle"
  geometry-node modifier, angle ~30–40°) so flat planes stay flat and only gentle
  curves smooth. Pixel's CRT case is this.

### The detachment bug — only subsurf *continuous* meshes

**Symptom (this project):** after joining limbs/head to the body and adding
Subdivision Surface, arms shrink away from the torso and the head floats off the
neck, leaving gaps.

**Cause:** Catmull-Clark subdivision contracts each *closed surface* toward its
interior. If the limbs are separate shells merely *intersecting* the torso (joined
into one object with `Ctrl+J` but **not welded** at the vertex level), each shell
is still topologically closed and independent. Subsurf shrinks each one around its
own volume, so the overlapping intersection that hid the seam pulls apart and the
gap appears.

**Fix — make it one continuous watertight surface before subdividing:**

1. Delete the faces where limb meets torso (open both shells at the junction).
2. **Bridge Edge Loops** (`Edge → Bridge Edge Loops`) between the two now-open
   loops, or merge-by-distance after aligning matching loops. The two must have
   the **same vertex count** on the joining loops — add/remove a loop so they
   match before bridging.
3. `Select All → Mesh → Merge → By Distance` (`M → By Distance`, threshold small,
   e.g. 0.0001) to weld any coincident verts.
4. Verify watertight: `Select All → Select → All by Trait → Non Manifold` should
   select **nothing** (no holes, no internal faces, no doubled edges).
5. *Now* add Subdivision Surface. One continuous surface subdivides as one volume;
   nothing detaches.

**Rule of thumb for the show:** never ship a subsurf character made of
intersecting primitives. Either weld everything into one manifold mesh, or turn
subsurf off and build hard-surface at final res. Disjoint + subsurf is the bug.

---

## 6. Modeling for the cel outline

The outline is an inverted-hull black shell (Solidify, flipped normals,
backface-culled black emission — see `cel-shading.md`). The mesh must be built to
play with it:

- **World-scale thickness → fix character height.** Outline thickness is in world
  units, so a character's apparent line weight scales with its size. **Set a fixed
  canonical height per character and apply scale** (see §8). Example convention:
  adult body height = a fixed number of Blender units, children scaled as a
  *modeled* proportion, not an object-scale change. Store the height in the asset
  README so every future shot inherits the same line weight.
- **Sharp vs soft edges drive where the hull reads.** The hull outlines the whole
  silhouette, but interior sharp edges (jaw line, case seams) can also catch line
  via Freestyle/crease. Mark genuinely sharp forms with `Mark Sharp` / crease;
  keep soft forms smooth so you don't get spurious interior ink.
- **Avoid razor-thin features and self-intersections.** The hull fails (inverts,
  flickers, or shows white backfaces) on fingers thinner than ~2x the shell
  thickness, on fully flat zero-volume cards, and where two surfaces interpenetrate.
  Fixes: give thin features real cross-section volume; separate the problem part to
  its own object with a thinner hull; or exclude it from the Solidify via a vertex
  group (Solidify has a `Vertex Group` limiter). See `cel-shading.md` §outline.
- **Consistent polygon scale.** Because the hull is uniform thickness, wildly
  uneven face sizes make the line look heavier over dense areas. Keep quads roughly
  even across a given character.

---

## 7. Head / face construction that reads in close-up

Replace the faceless sphere/cube with real facial architecture. Even stylized, the
eye reads these forms:

- **Brow ridge:** a modeled bony ridge above the eyes (§3 brow loops). Without it
  the forehead is a dead curve and the character can't emote.
- **Eye sockets:** actual recessed sockets, not eyes stuck on a surface. The lid
  loops wrap *into* a socket so the eyeball sits in a pocket and the lids have
  somewhere to close to.
- **Mouth bag + corners:** the mouth is a recessed tube (§3), with built-up corner
  junctions so smiles/frowns pull cleanly. The current blob has a painted-on line
  at best; a modeled bag is what lets visemes and expressions work.
- **Cheek / nose transition:** loops tie nose → cheek → mouth so a smile raises the
  cheek mass, not just the lip.

### Eyes: spheres-in-sockets vs flat anime eye-cards

Two valid approaches; choose per character and document it:

- **Proper spheres in sockets.** A UV-sphere eyeball rotates in the socket; lids
  are lid loops that follow it. **Pros:** true parallax, catchlight moves
  correctly, reads in 3/4 and profile, easy to aim with a track constraint.
  **Cons:** more rig (eye aim + lid follow), lids must be modeled to ride the
  sphere, more shape-key work.
- **Flat anime eye-cards.** A flat/slightly-curved plane in the socket with the eye
  drawn as a texture or shape-keyed geometry, slid around via UV offset / shape
  keys (the Murder Drones / anime approach). **Pros:** cheap, extremely
  on-style, huge expressive range (giant pupils, shapes), trivially art-directable.
  **Cons:** breaks in profile (the card is flat), needs a shrinkwrap/curve to the
  face so it doesn't look pasted on, every expression is author-driven not physical.

**For a stylised production:** flat eye-cards for the anime-register cast (cheap, on-target,
expressive); sphere eyes only where a character needs convincing 3/4-to-profile eye
contact in a hero shot. Pixel's screen-face is its own case — an emissive plane with
viseme/expression states, not a modeled mouth or eye at all (see `cel-shading.md`
for the emissive-blowout fix).

---

## 8. Naming, transforms, mirror, organization

Discipline here is what makes a locked, reusable asset instead of a liability:

- **Mirror workflow.** Model one half: delete the -X half, add a `Mirror` modifier
  (axis X, `Clipping` ON so centre verts weld to the seam, `Merge` ON). Keep it
  live through the whole model so both sides stay symmetric. **Apply it only at the
  end**, right before adding shape keys (you cannot add a Mirror-dependent shape
  key cleanly after applying asymmetric keys). After apply, run `M → By Distance`
  on the centre seam.
- **Apply transforms.** Before rigging/locking: `Ctrl+A → All Transforms` (or at
  least Rotation & Scale) so object scale = 1,1,1 and rotation = 0. This is
  *mandatory* for the outline (world-scale thickness assumes applied scale) and for
  clean rig deformation and modifier behavior. A character left at scale 1.7 will
  ink at the wrong weight and deform oddly.
- **Origin.** Set the character origin to the feet/floor center (`Object → Set
  Origin → Origin to 3D Cursor` with cursor snapped to world origin at the feet) so
  placement in a shot is predictable.
- **Naming.** Object names are the asset's API: `DILL_BODY`, `DILL_EYE_L`,
  `DILL_EYE_R`, mesh data `DILL_BODY_mesh`, the rig `DILL_RIG`, materials
  `DILL_skin_toon`, `OUTLINE_black` (shared). Parent all parts under the rig /
  an empty `IVY`. Put outline-shell objects / modifiers consistently named so a
  shot-assembly script can find them.
- **Collections.** One collection per character (`CHAR_DILL`) holding body, eyes,
  rig, props. Append the *collection* into shots, never individual objects.

---

## 9. Concrete build order (box-model, subsurf character)

1. **Reference.** Load front + side model-sheet images as background/reference
   images, aligned and locked. Match proportions to the sheet, not to a primitive.
2. **Blockout.** Rough the big masses as a *single* box-modeled cage (one object
   from the start — do not join primitives later). Nail proportion and silhouette
   against the sheet.
3. **Mirror on.** Delete -X, add Mirror (Clipping+Merge). Work one half hereafter.
4. **Head topology.** Build eye rings (3–4 loops), mouth bag (3–4 loops), brow
   loops, nose→cheek→mouth flow. Resolve excess loops with poles in hidden spots
   (§4). Carve eye sockets and mouth bag.
5. **Body topology.** Extrude limbs *from the torso's own geometry* (so it is one
   continuous surface — never a separate cylinder). Add 2–3 deform loops at each
   joint. Keep quads even.
6. **Eyes.** Add eye-cards or sphere eyes into the sockets as separate named
   objects; shrinkwrap cards to the face curve.
7. **Watertight check.** `Select → All by Trait → Non Manifold` = empty (§5.4).
8. **Apply Mirror**, weld seam (`M → By Distance`).
9. **Subsurf** (if used) level 1/2; tune sharpness with support loops/creases (§5).
10. **Apply transforms** (`Ctrl+A → All Transforms`), set origin at feet (§8).
11. **Materials:** assign toon node group + outline Solidify modifier
    (`cel-shading.md`).
12. **Shape keys** (visemes + expressions) — now that Mirror is applied.
13. **Rig** (`rigging.md`), weight-paint against the deform loops.
14. **Turnaround + model sheet:** render 8 angles + an expression row; this is the
    canonical check for every future shot.
15. **Lock:** save `assets/chars/<name>.blend` with named `*_RIG`; store canonical
    height, palette hexes, and outline thickness in the asset README.

---

## Verify

A model passes only if **all** of these hold:

1. **Subsurf without detachment.** Toggle Subdivision Surface on at render level.
   Nothing shrinks, no limb/head gap appears. `Select → All by Trait → Non Manifold`
   selects nothing. (If a gap appears, the mesh is still disjoint islands — §5.)
2. **Black-silhouette read.** Render the character as a solid black shape (all mats
   → black emission, flat light) at its hero camera. It must be instantly
   recognizable and appealing in pure silhouette; no mushy blob outline.
3. **Deform-loop check.** Bend every major joint ~90–120° and open/close the mouth
   and eyes via the rig/shape keys. No pinching, no volume collapse, no loop tearing
   at mouth corners or eyelids. Poles stay off the creases and out of highlights.
4. **Topology audit.** Mesh is quad-dominant; every pole sits in a hidden,
   low-deform spot; concentric loops ring both eyes (3–4) and the mouth (3–4); no
   loop terminates inside the eye or mouth ring.
5. **Outline weight.** Object scale is 1,1,1 (applied); character matches its
   canonical height; the inverted-hull line weight matches the other cast members
   at the reference camera distance.
6. **On-model.** Diff the turnaround against the locked model sheet — proportions,
   facial forms (brow, sockets, mouth bag), and palette match.

If any fail, it is still a blockout. Fix before locking the `.blend`.

## Verified (proof)
Applied to a production hero "Ivy" (13 Oct 2026). The prior face boolean-carved
deep eye sockets then subsurfed them, which rounded the socket rims into detached
goggle-rings around flattened eyeball spheres — plus a subsurfed nose-blob and a
floating mouth-bar. Rebuilt per this skill: **flat anime eye-cards flush on the face**
(thin-in-depth white disc + smaller proud iris disc, no carved sockets), a minimal
nose kept small enough that subsurf doesn't blob it, and a flush thin mouth. Result
went from uncanny-reject to a clean, expressive, on-silhouette stylized face that
passes the three-reads at hero close-up. Lesson reinforced: **do not boolean-carve +
subsurf deep sockets on a stylized cel face; flat flush eye-cards read cleaner and stay
inside the silhouette at 3/4** (a too-proud feature pokes past the outline as a floating
artifact — the removed upper-lid bar was exactly this).

---
id: creative-arts.animation.production-design.prop-design
name: prop-design
category: creative-arts
field: animation
product: production-design
tags: [prop-design, props, hero-prop, set-dressing-prop, silhouette, shape-language, scale, wear, patina, model-sheet, locked-asset, prop-continuity, cel, npr, blender]
level: advanced
status: draft
description: "Design hero and dressing props that read in silhouette and support story: shape language, scale, wear/history, cel model-ability, and locked-asset continuity."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Prop design — objects that read, belong, and carry story

A prop is any object a character handles or a set contains. Good prop design does three
jobs at once: it **reads instantly in silhouette**, it **belongs to the world** (per the
production-design charter, `creative-arts.animation.production-design.production-design`),
and it **carries story** — status, history, character. On a cel-shaded pipeline it must
also **model cleanly to flat read** and **lock for reuse** across every shot it appears
in. This skill covers both *hero props* (the detective's lighter, the cursed pocket watch —
things the camera and story care about) and *dressing props* (the mugs, cans, tools that
populate a set; see also `set-dressing`).

## 1. Classify the prop — the spec follows from the class

Decide the class first because it sets how much design and polish the prop earns:

- **Hero prop.** On-screen in close-up, handled, plot-relevant. Full design: silhouette
  study, multiple angles, wear states, maybe variants. Lock it hardest — it will be
  scrutinized frame by frame.
- **Mid prop.** Handled but not plot-critical (a character's everyday coffee mug). One
  clean design, one wear state, locked.
- **Dressing prop.** Populates the set, rarely in focus. Design for silhouette and world
  fit only; built into reusable dressing kits (`set-dressing`). Over-designing these is
  wasted effort and farm time.

Mis-classifying wastes budget both ways: a hero prop treated as dressing reads cheap in
close-up; a dressing prop treated as hero burns modeling hours no one sees.

## 2. Silhouette first — the one-value test

A prop must read as *what it is* with all internal detail removed. Process:

1. Design the outline in flat black at roughly the size it occupies on screen. A 1980s
   rotary phone, a thermos, a revolver — each must be unmistakable as a pure shape.
2. Run the **thumbnail test**: shrink the silhouette to ~64 px. If you can't name it,
   redesign the outline before adding any detail. This matters doubly in cel/NPR, where
   flat fills mean the silhouette *is* most of the read.
3. Avoid silhouette collisions: if the hero's hip flask and his lighter read the same at
   a glance, the audience misreads the action. Differentiate by proportion or a single
   distinctive notch.
4. Give hero props a **signature profile line** — one memorable contour (the hooked
   handle, the dented corner) that makes it recognizable from any distance and across
   cuts. That line is also what sells continuity.

## 3. Shape language and character

Shapes carry meaning before anyone reads detail: **round = safe/friendly/old-and-worn,
square = stable/official/institutional, angular = dangerous/modern/aggressive.** Use the
grammar deliberately:

- Match the prop's shape bias to its role and owner. The kindly diner owner's objects are
  rounded and soft-cornered; the mill foreman's are hard, rectilinear, utilitarian.
- Props extend character design. A fussy character owns fussy, over-maintained objects;
  a broken character owns broken ones. The prop is costume for the hands.
- Keep the shape language consistent with the world's architecture language (§3 of
  production-design) so props and sets feel designed by the same hand.

## 4. Scale — pin it to the human reference

Wrong scale is the most common and most spell-breaking prop error. Enforce it:

1. Model every prop against the project's **scale reference .blend** (canonical human
   height, 0.9 m doorknob, 0.75 m table). A mug is ~0.1 m tall; a revolver ~0.25 m; a
   rotary phone ~0.23 m wide. Write the real-world dimension in the prop's asset note.
2. Check scale **in a staged context**, not in isolation — a prop that looks right alone
   can be comically wrong in a character's hand. Parent it to the hand/eye-level rig and
   look.
3. For hero props handled on camera, confirm the grip works with the character rig's hand
   before locking; a prop the rig can't hold cleanly costs re-animation.

## 5. Wear, history, and patina — design the object's biography

A prop with no history reads as a 3D asset, not a thing someone owns. Give each prop a
one-line backstory and express it physically:

- **Use-wear localized to contact points**: the mug's rim chip where it hits the sink, the
  revolver's bluing worn off the grip, the phone's most-dialed numbers rubbed faint.
  Random dirt reads as noise; *localized* wear reads as a life.
- **Patina matched to the world's economy**: in a failing mill town, repairs are make-do
  (duct tape, rust, mismatched parts), not clean restoration. Wear is a storytelling and
  on-world device at once.
- **In cel/NPR, bake wear as a few flat shapes, not photoreal texture.** A chip is a small
  added facet or a painted mark in the base-color map; a scuff is a second darker fill
  region, not a noisy roughness map (which EEVEE Next's cel setup won't read anyway). Keep
  wear in the same limited palette and line language as the rest of the show.

## 6. Model-ability for the cel pipeline

Design with the renderer in mind so the prop holds up as a flat cel object:

1. **Clean, closed silhouette geometry** — no gaps that break the outline/Freestyle or
   inverted-hull line pass. The prop's profile edges must be hard enough to catch a line.
2. **Deliberate normals and bevels.** Cel shading banding keys off normals; a prop needs
   intentional, slightly beveled hard edges (not perfectly sharp, which flickers, not
   round, which muddies the light terminator). ~1–2 mm bevels on hero-prop edges.
3. **Limited material slots** that map to the show's cel ramp library, so the prop lights
   consistently with everything around it (pairs with `cel-shading` / `look-development`).
4. **Face the camera.** Design detail where the shots will see it; don't model what never
   points at lens. Budget polygons by class (§1).
5. **Origin and orientation** set for rigging/pickup: origin at the natural grip or base,
   axis aligned, real-world scale applied (scale = 1.0) before lock.

## 7. Locking and prop continuity across shots

The whole pipeline's consistency depends on a prop being **one locked asset reused
everywhere**, not re-modeled per shot.

1. **Lock the master .blend**, register it in the production-design asset registry
   (thumbnail, real-world scale, material IDs, owning character, shots it appears in).
2. **Link, don't append** the prop into shot files so one fix propagates. If a shot needs
   a different state, make it a *variant* of the master (e.g. `watch_intact` /
   `watch_cracked`), not a new object — and register the variant and the shot/sequence
   where the state changes.
3. **Track state across the sequence** (full/empty, intact/broken, on/off). This is the
   core of `continuity-supervision`: the prop's state must march correctly with the story,
   and a cut must not reset it (the glass that's half-full, then full, then half again).
4. **Guard hand-off between shots and departments**: the prop a character sets down in
   shot A must be where they pick it up in shot B — screen position and state both.

## 8. Worked example — a hero pocket watch across a mystery

A cursed pocket watch is the plot engine of a cel series, so it earns full hero treatment:

- **Silhouette.** A clean circle with a hooked bow and a short fob chain — unmistakable at
  64 px and distinct from the detective's round lighter (the watch reads *wider* with the
  chain, the lighter is a plain rounded rectangle). Signature line: the cracked case hinge.
- **Shape language.** Round and old — it belongs to the dead, to the past the town can't bury;
  its softness contrasts the hard rectilinear mill props of its antagonist.
- **Scale.** ~0.05 m case diameter, modeled against the scale reference and test-held in the
  rig's hand before lock — a watch too large reads as a toy, too small won't sell in close-up.
- **Wear/history.** Bluing worn off the bow where a thumb opens it; the engraving on the back
  rubbed faint; baked as flat cel shapes in the show palette, not noise maps.
- **Model-ability.** Closed silhouette so the line pass catches the case; ~1 mm bevels on the
  case rim; two material slots (brass ramp, glass ramp) from the show library; origin at the
  bow for clean pickup; scale applied to 1.0.
- **Variants and state.** `watch_closed`, `watch_open`, and `watch_cracked` are registered
  variants of one locked master. The crack appears in SEQ 06; from there every shot links
  `watch_cracked`, and the continuity log tracks open/closed state per shot so a cut never
  un-cracks it. One master, linked (not appended) into every shot it touches.

## Verify

- [ ] Each prop is **classified** (hero / mid / dressing) and designed to the right depth
  for its class.
- [ ] The prop **passes the ~64 px silhouette test** and does not collide in silhouette
  with other nearby props; hero props have a signature profile line.
- [ ] **Shape language** matches the prop's role and owner and the world's architecture
  grammar.
- [ ] The prop is built at **real-world scale against the scale reference** and checked in
  a staged context / in the rig's hand.
- [ ] Wear is **localized to real contact points**, matched to the world's economy, and
  baked as flat cel shapes in the show palette — not photoreal noise.
- [ ] Geometry is **cel-clean**: closed silhouette, intentional ~1–2 mm bevels, material
  slots mapped to the show ramp library, scale applied (1.0), sensible origin/orientation.
- [ ] The prop is a **single locked master** in the asset registry, **linked** (not
  appended) into shots; alternate states exist as registered **variants**.
- [ ] Prop **state is tracked across each sequence** and hands off correctly between shots
  (position and state continuous across cuts).

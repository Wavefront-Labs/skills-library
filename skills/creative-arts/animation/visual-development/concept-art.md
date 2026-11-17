---
id: creative-arts.animation.visual-development.concept-art
name: concept-art
category: creative-arts
field: animation
product: visual-development
tags: [concept-art, visual-development, vis-dev, thumbnails, design-exploration, environment-concept, keyframe, composition, value-study, color-study, mood, iteration, pre-production, thumbnailing]
level: advanced
status: draft
description: "Explore and lock a show's visual ideas before the build: thumbnails, design exploration, value/color studies, and keyframes that de-risk the 3D."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Concept Art / Visual Development — explore cheap before you build expensive

Vis-dev is where visual decisions are made **in minutes on paper, not in days in
Blender.** The cardinal production error — and the one an automated pipeline commits by
default — is *building the first idea*: modeling and lighting a shot before anyone
explored what it should look like. A faceless blob in a blown-out set is what you get
when the model is the first draft. Concept art is the cheap exploration that prevents
it, and the contract the expensive 3D step then renders to.

## 1. Thumbnails first — quantity breeds quality
Design is a search problem, and the first idea is almost never the best; it's the most
obvious. Flood the space with options before committing:
1. **Go small and fast.** 100-200px, 30-90 seconds each. You are exploring *shape,
   value, and composition relationships*, not rendering. If a thumbnail takes more
   than two minutes you're finishing, not exploring.
2. **Produce 10-30 per subject** (character, prop, environment, or key shot). The cost
   of a bad idea at thumbnail scale is seconds; the cost of discovering it after
   modeling is days.
3. **Explore along deliberate axes**, not random doodles: silhouette / shape-language
   variants (round vs angular vs tall), proportion variants, value-layout variants
   (where the darks and lights group), and staging/camera options. Varying one axis at
   a time makes the comparison legible.
4. **Squint test.** A thumbnail that reads at squint — subject instantly separable from
   ground — survives. One that goes to mush fails, no matter how nice the detail.
5. **Select 2-3 to push**, against the show bible, with the art director. Kill the rest
   without mourning; that's what they were for.

## 2. What vis-dev delivers (the pre-production artifacts)
- **Character concepts** → feed character-design-craft (appeal, shape language) and the
  model sheet. Vis-dev finds the design; design-craft refines it to spec.
- **Environment / set concepts** → the mood, scale, materials, and key composition of a
  location before it's modeled, so set-building has a target, not improvised geometry.
- **Prop / vehicle concepts** → shape and read for hero props (the orange, the meter,
  the hand-painted sign) that the story turns on.
- **Keyframes (production illustrations)** → fully-rendered paintings of the most
  important story moments at the show's final-look bar. A keyframe is the **proof the
  look is achievable** and the north star for lighting/comp — "make the shot look like
  this." One strong keyframe per sequence is worth more than a pile of models.
- **Callout / detail sheets** → how a tricky material, FX, or mechanism reads close up.

## 3. Value studies before color
Value (lightness) carries read; color carries mood. Solve them in that order:
- **Three-value block-in.** Reduce each key shot to three values — dark, mid, light —
  and assign each depth plane (foreground / midground / background) its own band. Cel
  work lives or dies on value separation; if it reads in three greys it will read in
  color.
- **Notan.** A pure black/white pass confirms the composition holds with color stripped.
  If the subject disappears in notan, no palette will save it.
- **Only then color.** Color studies set temperature and the limited palette per
  location (warm-saturated town vs cold gray-green alley), tying to the color-script.
  Keep color choices subordinate to the value structure already locked.

## 4. Design exploration by asset type
Each deliverable is explored differently:
- **Characters:** start from silhouette-only shapes (fill black, no interior) and judge
  read and appeal before any detail — if the black shape doesn't say "anxious kid" or
  "smiling predator," no costume fixes it. Then explore proportion (head-to-body),
  shape-language family (Dill all soft rounds, Chip all sharp wedges so the ensemble
  reads as a system), then colour. Push 2-3 silhouettes to a turnaround-ready sketch.
- **Environments:** explore the *key shot* of the location, not a floor plan. Thumbnail
  the mood, the dominant lines, foreground framing, and the one hero element the beat
  turns on. Settle scale and material feel here so set-building models to a target.
- **Props:** explore read-at-distance first (a prop the plot hinges on must be legible
  in a wide), then detail. Design hero props (the meter, the orange, the sign) for a
  clear silhouette and one memorable colour note.

## 5. The keyframe (the final-look proof)
A keyframe is a finished painting of a pivotal story moment at the bar the show must
hit. It is the most expensive vis-dev artifact and the most valuable:
1. Pick the one shot per sequence that, if it looks right, proves the sequence works.
2. Paint it to final quality — lighting, palette, line, atmosphere, character in situ.
3. Use it as the **north star**: lighting and comp match the keyframe; the 3D shot is
   judged against it side-by-side. "Make the shot look like this" is a decision already
   made, not a debate during the render.
A single strong keyframe de-risks a whole sequence better than ten half-finished model
turnarounds.

## 6. Iteration cadence & detail economy
- **Resolve big before small.** Composition → value → colour → detail, in that order;
  never polish rendering on a layout that isn't locked.
- **Detail only where the eye goes.** A concept reads by a few sharp focal accents
  against larger quiet areas; even detail everywhere is the amateur tell and reads flat.
- **Review against the bible each round**, kill what drifts, and keep selected
  concepts + keyframes in `<REPO>/series/design/ref/` so build and review share one
  reference.

## 7. Composition & staging in concept (so shots aren't improvised)
Concept the key shots, not just the assets:
- **Design the frame:** where the subject sits, foreground/mid/background depth, where
  the eye enters and travels, value grouping per plane.
- **Lead the eye** with the architecture — converging lines, framing elements, a light
  shaft — toward the subject.
- **Pick the lens feel** (wide establishing vs intimate close) and camera height
  deliberately; these become real camera values downstream.
- **Design the background to support and separate** the subject — never a flat blown
  field. A readable concept background gives the 3D shot a target instead of a default.
- **Negative space** for the subject to read against; resist filling every corner.

## 8. The explore-before-build discipline (agent pipeline)
In an automated/agent build, vis-dev is the gate that forces a decision *before*
geometry exists:
1. Generate thumbnail options.
2. Select against the bible (value, shape, palette, read).
3. THEN model/stage to the chosen concept — never let "render the default" be the
   design decision.
4. Keep the selected concept + the sequence keyframe beside each asset/shot in
   `<REPO>/series/design/ref/` as its build target and review reference, so the Blender
   build script and the review both point at the same image.

## Verify
- [ ] Each hero character/set/shot has a small set of explored thumbnail variations on
      record, not a single first-idea.
- [ ] A notan / three-value study exists for each key shot and holds at squint.
- [ ] Value was solved before color; color stays subordinate to value structure.
- [ ] 2-3 options were selected against the show bible before anything was modeled.
- [ ] At least one fully-rendered keyframe exists per sequence at the final-look bar,
      used as the lighting/comp north star.
- [ ] Every concept's background is designed to support the subject (no blown fields).
- [ ] The built asset/shot visibly matches its selected concept side-by-side.

See look-development (the bar concepts serve), color-script (value/temperature),
character-design-craft (refines the chosen character), environment set-building,
camera-cinematography, compositing-grade.

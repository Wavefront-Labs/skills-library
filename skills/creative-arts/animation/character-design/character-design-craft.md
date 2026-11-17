---
id: creative-arts.animation.character-design.character-design-craft
name: character-design-craft
category: creative-arts
field: animation
product: character-design
tags: [character-design, silhouette, shape-language, appeal, proportion, head-heights, line-of-action, contrast, exaggeration, asymmetry, cel, toon-ramp, thumbnail-read, model-ability, topology, murder-drones, primitive-shapes, silhouette-read-test, head-count, rig-friendly-design, character-brief]
level: advanced
status: draft
description: "Design appealing, on-model, model-able stylized characters for a 3-tone cel pipeline: shape language, silhouette, proportion, contrast, model-ability."
sources:
  - "Preston Blair, Cartoon Animation (construction, shape)"
  - "Walt Stanchfield, Drawn to Life vol. 1-2 (line of action, appeal)"
  - "Tom Bancroft, Creating Characters with Personality (shape language, silhouette)"
  - "Andrew Loomis, Figure Drawing for All It's Worth (head-height proportion systems)"
licence: Apache-2.0
version: 6
updated: 2026-11-17
aliases: []
---

# SKILL: Character design craft (expert)

The craft of turning a brief into a form that reads in one frame, survives a 3-tone
cel ramp at thumbnail size, carries personality in its shape, and can actually be
modelled with clean topology and rigged. This is the design *authority* for the production — output locks into `model-sheet-turnaround`, gets built in
`creative-arts.animation.blender.character-blockout`, shaded by
`creative-arts.animation.blender.cel-shading`, and reused untouched every shot.
If this step is weak, every downstream skill inherits a blob.

Primitive-blob failure is the default outcome of *not* doing this craft. The rest of
this file is how you avoid it.

---

## 1. Design from the brief, not from the pencil

Before a line: write the character's **want, flaw, role, and one-word essence**. Design
is characterisation made visible — every choice below must trace to one of those four.

- Ivy = outsider / awake → *unfinished*: slightly asymmetric, softer edges, one
  "wrong" proportion vs the town's manufactured regularity.
- Pixel = the show's host → *warmth hiding a crack*: friendly retro-TV, boxy screen face,
  one detail (a hairline screen-crack) that only appears for a single frame.

If you cannot name what a shape *says* about the character, it is decoration. Cut it.

---

## 2. Shape language (the grammar)

Three primitives, three reads. This is not decoration theory — it is how an audience
assigns personality before they consciously look.

| Shape | Reads as | Use for | Overuse failure |
|-------|----------|---------|-----------------|
| **Round / circle** | friendly, soft, safe, young, harmless | heroes, comic relief, children, anything you want liked | mush — no structure, forgettable |
| **Square / rectangle** | stable, reliable, strong, honest, *or* dull / institutional / immovable | authority, the dependable one, the system/town | stiff, boring, reads as "prop" |
| **Triangle / wedge** | dynamic, dangerous, sharp, unstable, aggressive | villains, threats, speed, the uncanny | spiky-for-its-own-sake, reads "generic bad guy" |

Rules that separate a designer from someone who read a blog post:

1. **One dominant shape per character, chosen from the essence.** Pixel = round body /
   square head (warm core, boxy broadcast face). Censors = triangle (broken, sharp,
   wrong). The town extras = square (manufactured, interchangeable, dead-eyed stable).
2. **A secondary shape is the nuance, not a second opinion.** Nana Wren = soft squares:
   square silhouette (solid, won't move, dry authority) with rounded corners (she is
   merciful underneath). The *ratio* of primary to secondary is the personality dial.
3. **Shape must echo through scale** — head, torso, hands, prop, accessory all carry the
   dominant shape. A round character holding a round mug, with round shoes, reads as a
   designed whole. Mixing shapes at random reads as noise.
4. **Contrast across the cast is a casting decision.** Line the ensemble up: if two
   characters share a dominant shape and a height, one of them is redundant. Spread the
   cast across the shape triangle the way you'd spread a vocal range.

---

## 3. Design in black first (the readability discipline)

**Fill the whole design solid black and look at it.** If the silhouette does not tell you
*who it is* and *what mood they're in*, no amount of colour, line or texture will save it.
This is the single most load-bearing habit in the craft.

- **Silhouette test, per character:** black fill at 100%. Recognisable? Does the pose read
  (line of action, §6)? Negative space between limbs and body — is it doing work, or is
  everything one dark mass?
- **Ensemble silhouette test:** every cast member in black, same row, same height box.
  No two may be confusable. Vary height, proportion, head shape, and *one* signature
  element (Pixel's antennae, Nana's bun, Ivy's lopsided collar). If you cover the colour
  and the detail and still name everyone, you have an ensemble. If not, you have variants.
- **Negative-space test:** a prop or a hand held *away* from the body creates a readable
  hole in the silhouette; a hand tucked against the hip disappears. Design the gaps.

Do colour, line weight and surface detail *only after* the black silhouette passes. They
are the last 20%, not the design.

---

## 4. Proportion systems (head-heights)

Measure everything in **head-heights** — the character's own head is the ruler. This is
how you keep a stylised cast internally consistent and how the modeller gets real scale.

- **2–3 heads** = cute / chibi / heavy cartoon (big head, stubby body; Pixel ≈ 2.5).
- **4–5 heads** = classic TV-toon, appealing stylised (Rick & Morty / Murder Drones zone).
- **6 heads** = "real-ish" stylised teen/adult (Ivy ≈ 5.5–6 — slightly taller, "awake").
- **7–8 heads** = heroic / realistic (rarely what a cel-shaded YouTube show wants).

Discipline:

1. **Pick the show's house ratio and hold the cast within one head of it.** A cast that
   ranges 2.5–6 heads is fine *if deliberate* (Pixel is a sidekick scale, Ivy is lead
   scale). A cast that drifts because each design was eyeballed separately looks broken.
2. **Lock sub-proportions as fractions of head:** eye-line, shoulder width, hand length
   (hand ≈ chin-to-eyebrow), leg-start, etc. These become the guide-lines on the
   turnaround (`model-sheet-turnaround` §proportion grid).
3. **Exaggerate the proportion that tells the story, pull everything else back.** Pick
   *one* heroic ratio (Pixel's oversized head-screen; Warden's elongated reach) and keep
   the rest neutral. Two competing exaggerations fight and read as a mistake.

---

## 5. Contrast & exaggeration (appeal is clarity, not prettiness)

**Appeal = a clear idea, confidently stated, with one focal point.** Ugly, scary and
comic characters all need appeal; appeal is not "cute", it is *legibility of intent*.

- **Contrast is the engine:** big head / small body, heavy top / spindly legs, dense
  detail cluster against large quiet planes, sharp accessory on a round form. A design
  with no internal contrast is the blob — uniform curvature everywhere, nothing to look
  at, nothing to animate.
- **Exaggerate, then simplify.** Find the defining feature and push it past life; strip
  everything that isn't carrying meaning. The eye needs one place to rest (the focal
  point: Pixel's screen-face, Ivy's eyes) and quiet everywhere else. Detail-soup —
  three competing focal points, even surface noise — is the second most common failure
  after the blob, and it makes the character impossible to keep on-model.
- **One focal point.** Rank features: #1 gets the most contrast, detail and colour accent;
  everything else supports. If two features both scream, the design has no face.

---

## 6. Line of action (implied motion in a static design)

Even a neutral standing pose must have a **single dominant curve** running head-to-toe —
the line of action. It is what makes a static turnaround feel alive instead of embalmed.

- Draw the line *first*, hang the body on it. A C-curve (relaxed, soft characters), an
  S-curve (elegant, sinuous, or sly), a straight diagonal (rigid, aggressive, or
  snapping to attention).
- **Fight symmetry with it.** A pure vertical, bilaterally symmetric standing pose reads
  dead — which is exactly right for the town's manufactured extras and exactly wrong for
  the leads. Give the leads a slight weight-shift / contrapposto so the line of action
  bends.
- The neutral *design* pose still needs a line of action even though the turnaround is
  orthographic (`model-sheet-turnaround` uses a relaxed A-pose, not a dead T-pose, for
  this reason).

---

## 7. Asymmetry (the life switch)

Perfect symmetry reads manufactured, institutional, dead. One deliberate asymmetry reads
*alive*. Use it as a tool, with intent:

- **One** signature asymmetry per character — a tilted antenna, a side-swept fringe, a
  single shoulder pad, a collar that sits crooked. More than one and it reads messy.
- **Symmetry is a characterisation choice, not a default.** The town extras
  are *deliberately* symmetric (the uncanny sameness is the point). The awake characters
  break it. The asymmetry carries theme.
- Note that a symmetric base mesh is cheaper to model and rig (mirror modifier); add the
  asymmetry as a *layer* (an accessory, a shape-key offset, a texture) so you keep the
  modelling economy without the dead read. Flag this to
  `creative-arts.animation.blender.character-blockout`.

---

## 8. Designing for a 3-tone cel ramp + outline

This is where generic "character design" advice stops and a production's pipeline begins.
The target shader (`creative-arts.animation.blender.cel-shading`) resolves lighting to a
**CONSTANT-interpolation ColorRamp** — base, one shadow, sometimes one highlight — plus an
inverted-hull outline. You are not designing for smooth rendering; you are designing for
**two or three flat tones separated by a hard terminator line, wrapped in a black
outline.** Design to that or the model fights the shader.

1. **Big, clean planes.** The terminator is a hard edge that sweeps across the form. On a
   large simple plane it draws a bold, readable shadow shape. On fiddly bumps it shatters
   into visual noise. Put detail in *silhouette and colour*, never in surface
   micro-geometry.
2. **Think in shadow shapes.** When you design, paint the predicted shadow as one flat
   region and ask: is that shape appealing on its own? The cel shadow is a design element,
   not a byproduct. Hard-edged drop of the brow over the eyes, a clean under-chin wedge.
3. **Value-separate the three tones *within the character* too.** Base, shadow and
   outline must each read as a distinct value. If base and shadow are too close in value,
   the terminator vanishes and the form goes flat; too far and it looks like dirt.
4. **Outline is brand and must be budgeted.** One world-scale line thickness per character,
   reused (`character-blockout` §outline). Design forms that look right *wearing* a line of
   that weight — tiny details thinner than the outline will be eaten by it.
5. **Local colour does the modelling the shader won't.** Since you only get 2–3 tones,
   adjacent parts must separate by *hue/value of flat colour*, not by rendered shading.
   Pixel's mint face against a darker body; Ivy's hair a clear value-step off the skin.

---

## 9. Readability at thumbnail size

The series ships on YouTube; the first contact is a 120px thumbnail and a scrubbed
timeline. **Shrink every design to ~64px tall and look.**

- Focal point still reads? Face still reads as a face (eyes + mouth resolve as marks, not
  mud)? Signature silhouette still unmistakable?
- If a detail disappears at thumbnail size, it is *not* a reading detail — it may stay for
  richness, but it must not be carrying the character's identity. Identity lives in
  silhouette, big shapes, and the one colour accent.
- This is also the distance test: if it reads at 64px it reads from the back of the room.

---

## 10. Model-ability (design so it can actually be built & rigged)

An "undrawable" design is a wish, not a design. You own the constraints of the build.

- **Clean topology intent.** Mark where edge-loops must run: rings around the mouth, eyes,
  and every joint that deforms (elbow, knee, shoulder, jaw). Avoid n-gon-forcing
  junctions — no spot where five features collide into one vertex. Hand this intent to
  `creative-arts.animation.blender.sculpt-retopo` / `character-modeling`.
- **Deformation room.** Leave geometry slack at every bending joint and at the mouth; a
  skin-tight sleeve at the elbow collapses the cel band into a crease
  (`creative-arts.animation.blender.rigging` warns the terminator exposes bad weights).
- **Rig-able face.** The face must be designable as **shape keys / blendshapes**, so decide
  now what the key poses are. The full expression vocabulary and the named blendshape set
  live in `expression-design` — design the face *to* that set, not to a one-off drawing.
- **No self-intersecting costume.** Overlaps that clip at rest will explode under
  deformation. Cloth must be sim-able or rig-able simply; flag anything that needs sim.
- **Mirror-friendly base, layered asymmetry** (§7) so the build stays cheap.
- **Shader-faced shortcut:** for a character like Pixel whose face is a drawn/emissive
  plane, "topology" of the face is a texture/driver problem, not a mesh problem — note it
  so the modeller doesn't waste effort retopo-ing a screen (`character-blockout` §face).

---

## 11. Worked critique: blob vs designed

**Weak (the primitive blob — current state):**
A UV-sphere head on a cube torso, two cylinder arms, rubber-hose legs. Uniform curvature,
uniform scale, bilateral symmetry, eyes as two black dots floating on the sphere.

- *Silhouette test:* black fill → an indistinct lump. Could be any of the cast.
- *Shape language:* sphere says "soft/young", cube says "stable" — but they're stapled
  together with no ratio or intent, so they say nothing. No dominant shape.
- *Contrast:* none. Every element is the same size and curvature → no focal point, the eye
  slides off. Face doesn't read because the eyes have no structural socket, brow or scale
  relationship to the head.
- *Cel ramp:* a sphere under a hard terminator gives a boring symmetric crescent shadow
  with nothing to say; the cube's flat planes flash fully lit or fully dark with no form.
- *Line of action:* dead vertical. Reads embalmed.
- *Thumbnail:* a grey pill. Zero identity.

**Strong (the fix):**
Keep the warm round core but make the **head a deliberate square-ish broadcast screen at
2.5 heads total** (big-head contrast), body a soft rounded wedge narrowing to small feet
(top-heavy contrast, round-dominant with a square accent). Eyes get a real brow-shelf and
a scale relationship (large, focal). One antenna tilted (asymmetry). Line of action is a
gentle forward-leaning C (eager, alive). Mint-green emissive face against a desaturated
body (colour separation the 3-tone ramp can't do on its own). A single LIVE-dot accent is
the one high-detail focal point; everything else is quiet plane.

- *Silhouette:* unmistakable even in black — square head, round body, tilted antenna.
- *Cel ramp:* big planes catch a clean readable shadow shape; the brow-shelf throws a hard
  designed shadow over the eyes.
- *Thumbnail at 64px:* reads instantly as Pixel, face resolves, accent pops.
- *Model-ability:* mirror-able body, face is an emissive plane (no retopo), antenna offset
  is the only asymmetry layer.

The difference is never "more detail". It is *shape intent, contrast, one focal point,
value separation, and a line of action* — applied on purpose.

---

## Verify

Pass/fail a design against the show bible. A design ships only when **every box is true**;
a single fail sends it back. A reviewer runs this in order:

- [ ] **Brief trace:** every major shape choice traces to want/flaw/role/essence (§1). No
      orphan decoration.
- [ ] **Black-silhouette solo:** fill 100% black — identity and mood read with zero colour
      or line (§3).
- [ ] **Black-silhouette ensemble:** in a row with the whole cast, no two confusable; one
      signature element each (§3).
- [ ] **Dominant shape** chosen and echoed through head/body/hands/prop; matches essence
      (§2).
- [ ] **Proportion in head-heights** stated, within one head of the house ratio, sub-ratios
      locked (§4).
- [ ] **One focal point;** features ranked; no detail-soup, no competing exaggerations
      (§5).
- [ ] **Line of action** present even in neutral; not a dead vertical unless the character
      is meant to read manufactured (§6).
- [ ] **Exactly one** deliberate asymmetry, or deliberate symmetry justified by theme (§7).
- [ ] **3-tone read:** mock the base + one shadow as flat regions — the shadow shape is
      appealing, base/shadow/outline are value-separated, no fiddly surface detail to
      shatter the terminator (§8).
- [ ] **Line-weight test:** forms still read wearing the character's locked outline
      thickness; nothing thinner than the line (§8).
- [ ] **Thumbnail test:** at ~64px tall, focal point + face + silhouette all still read
      (§9).
- [ ] **Model-able:** loop/deformation intent marked, mirror-able base, face expressible as
      the named blendshape set, no self-clipping costume (§10, `expression-design`).
- [ ] **Lockable:** proportions (heads), dominant+secondary shapes, palette hex,
      material/emissive notes, and a do/don't list are all written down so it reproduces
      forever.

**Runnable check (3-tone + thumbnail, no DCC needed):** take the flat colour comp, posterise
it to 3 levels (`magick in.png -posterize 3 cel.png`) and separately desaturate +
downscale to 64px (`magick in.png -colorspace Gray -resize x64 thumb.png`). If the character
still reads as itself in *both* outputs, it passes §8–§9; if either goes to mud, it fails.

---

## Pitfalls

- **The blob:** primitives stapled together with no dominant shape, no contrast, no focal
  point, dead symmetry. Diagnosis in §11. This is the default; kill it on purpose.
- **Detail soup:** no focal hierarchy, surface noise, nothing to rest on → impossible to
  keep on-model and dies at thumbnail size.
- **Hue-only colour:** separation that vanishes in grayscale / on a bad monitor / under the
  cel ramp. Always value-separate.
- **Surface micro-detail** that shatters the hard cel terminator — detail belongs in
  silhouette and colour.
- **Symmetry everywhere** → embalmed; only correct when the character is meant to read
  manufactured.
- **Pretty from one angle, unmodelable from every other** — design is a 3D object, not a
  pin-up (that's why `model-sheet-turnaround` exists).
- **Not locking hex/proportions** → drift across shots, the #1 consistency killer.

Next: define the facial acting in `expression-design`, then lock everything into
`model-sheet-turnaround`.

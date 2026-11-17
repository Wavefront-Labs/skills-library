---
id: creative-arts.animation.production-design.production-design
name: production-design
category: creative-arts
field: animation
product: production-design
tags: [production-design, art-direction, visual-world, show-bible, visual-motif, period, place, culture, continuity-bible, every-frame-on-world, scale, architecture, cel, npr]
level: sme
status: draft
description: "Design a film's whole visual world: place/period/culture logic, theme-carrying motifs, the consistency bible, and the every-frame-on-world discipline."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Production design — designing the whole visual world

Production design is the discipline that decides **what the world is made of and why**,
so that every prop, costume, set, and background in the film belongs to one coherent
place that could not be any other place. It is distinct from look-development
(`creative-arts.animation.art-direction.look-development`), which sets the *render bar* —
how line, light, and palette are executed. Production design sets the *world bar*: the
internal logic that makes a water tower, a coffee mug, and a character's coat read as
coming from the same town, period, and economy. Look-dev makes it look like one show;
production design makes it feel like one place. On a feature you have both; on a small
cel series like a stylised series one person often wears both hats, which is exactly why the
two disciplines must be kept conceptually separate — you review for "on-model" (look-dev)
and "on-world" (production design) as two different passes.

The deliverable is not pretty pictures. It is a set of **decisions, written down and
pinned**, that every downstream artist (and every automated pipeline step) can obey
without re-deciding. A consistent world built from locked `.blend` assets is only as
coherent as the design logic those assets were built from.

## 1. Establish the world's governing logic first (the "world bible")

Before a single asset is modeled, answer and *write down* the four axes. Vague answers
here cause expensive re-dressing later.

1. **Place.** Not "a town" — a specific geography. Example: a fog-pocketed logging
   valley in the Pacific Northwest, a dead-end at the foot of a mountain, one road in.
   Geography dictates light (low sun, long shadows, fog diffusion), materials (damp cedar,
   rust, moss), and architecture (steep roofs to shed rain, raised foundations).
2. **Period.** Pin a decade and *freeze the technology set*. Example: late-1980s —
   so rotary and early push-button phones, CRT TVs, no cell phones, station wagons. Write
   a **"what exists / what does not exist" list.** This single list prevents the most
   common on-world failure: a prop from the wrong era slipping into a set-dressing kit.
3. **Culture & economy.** Who lives here, what pays the bills, what's the social order?
   A failing mill town reads in frayed signage, make-do repairs, and empty storefronts —
   wealth and poverty are *designed*, not accidental. This drives wear and set-dressing.
4. **Genre & tone.** Cozy mystery vs. horror vs. comedy changes the same valley
   completely. Tone sets your contrast range, your palette temperature, and how much
   negative space a frame carries.

Capture these as a one-page charter plus a reference board of 15–30 real-world frames
(not other cartoons — actual photographs of the real place/period). This is your appeal
to reality; stylization comes *after* you know the truth you're stylizing.

## 2. Build visual motifs that carry theme

A motif is a repeated visual idea that the audience absorbs without naming. Good
production design makes the *theme* visible in the furniture. Process:

1. State the film's theme in one sentence ("a town clinging to a dead industry can't let
   its dead rest"). 
2. Derive 3–5 concrete motifs that embody it: in a worked example, (a) **things covered
   over** — tarps, dust sheets, boarded windows, fog; (b) **verticals that don't quite
   reach** — half-built structures, a mill crane frozen mid-lift; (c) a recurring
   **amber light in the dark** (one warm window per wide, the only hope-color).
3. Assign each motif a rule a modeler can follow: "every exterior wide has exactly one
   amber practical visible; everything else is cold." Motif without a *rule* evaporates
   under production pressure.
4. Track motif presence per sequence in the continuity bible so it doesn't vanish in
   the middle act where the theme matters most.

Motifs also give you cheap continuity: reusing the same three shapes everywhere is both
thematically rich and pipeline-efficient (fewer unique assets to model and lock).

## 3. Scale and architecture language

Decide the world's **measurement grammar** and enforce it so reused assets slot together.

- **Human reference.** Fix a canonical character height (e.g. 1.75 m) and build a scale
  reference .blend with a standing figure, a 0.9 m doorknob line, a 0.75 m table, a
  2.1 m door. Every set and prop is checked against it. Mismatched scale is the fastest
  way a reused asset breaks the world.
- **Architectural ruleset.** One structural vocabulary: roof pitch range, window
  proportion (e.g. tall 1:2.2 sashes), a limited material palette (cedar clapboard,
  corrugated steel, cinder block for the mill). Write it as a modeler's checklist.
- **Silhouette hierarchy.** Decide what shapes the town skyline (the mill, the water
  tower, the church spire) and keep hero silhouettes distinct from background filler.
- **Modularity.** Design to a grid (e.g. 1.2 m wall module) so set pieces recombine into
  new locations without new modeling — essential when a locked-asset pipeline reuses the
  same `.blend` library every shot (pairs with `set-building`).

## 4. The consistency bible (the artifact that scales)

The bible is the single source of truth. Structure it as:

- **Charter** (the four axes from §1) and the exists/doesn't-exist list.
- **Motif sheet** with the per-sequence rules.
- **Asset registry**: every locked `.blend` with a thumbnail, canonical scale, material
  IDs, and the shots/sequences it appears in. This doubles as the continuity-tracking
  spine (pairs with `continuity-supervision`).
- **Palette & material board**: keyed to the color-script
  (`creative-arts.animation.art-direction.color-script`) — which materials/colors are
  allowed per location and per time-of-day.
- **Review bar**: the on-world checklist (below) applied at design review *and* at
  pre-render.

Pin it, version it, and never let a shot proceed from design on a verbal decision — if
it isn't in the bible, it isn't decided.

## 5. How design supports story and emotion

Design is dramaturgy by other means. Concrete levers:

- **State change across the film.** The same kitchen in act 1 (warm, cluttered, lived-in)
  and act 3 (cold, stripped, one chair) tells the arc without a line of dialogue. Plan
  **location state variants** up front and store them as asset variants (pairs with
  `set-dressing` and `costume-design` variants).
- **Staging-aware design.** Design sets so the blocking the director wants is *possible*:
  a clear eyeline path, a place for the hero to stand apart, a doorway that frames.
  Coordinate with `layout-blocking` and `camera-cinematography` — design that fights the
  camera gets redressed on the floor, which is waste.
- **Information control.** What the audience learns and when is a design decision: the
  boarded room you see in episode 1 and enter in episode 6. This ties design to
  `shot-episode-structure`.
- **Emotion via contrast.** Reserve your strongest contrast, warmest color, or most open
  negative space for the emotional peak; if every frame is loud, the peak has nowhere to go.

## 6. Collaborating across the art pipeline

Production design sits above and coordinates the specialist crafts, each of which has its
own skill: `concept-art` (exploration), `prop-design`, `costume-design`, `set-dressing`,
`background-painting`, `set-building`. The flow:

1. Design charter + motifs + scale language (this skill).
2. Concept art explores within the charter; approved concepts become design intent.
3. Specialists execute: props, costumes, sets, backgrounds — each checked against the
   charter and the bible.
4. Look-dev sets how they render; color-script sets their palette per beat.
5. Layout/camera stage them; editorial cuts them; continuity-supervision guards them.

Your job at each handoff is to answer "does this belong to our world?" and send back
anything that doesn't, with a specific reason tied to the charter — never "I don't like
it," always "late-80s logging town wouldn't have that; swap for X."

## 7. The "every frame on-world" discipline

The bar is simple and absolute: **pause on any random frame and nothing in it should
contradict the world.** This is where features earn their polish and where cheap
pipelines fail. Practice:

- Do **spot-pause reviews**: grab 10 random frames across the reel and check each against
  the on-world checklist. One anachronism, one wrong-scale prop, one off-palette set
  piece breaks the spell.
- Guard the **edges and backgrounds** hardest — hero props get attention automatically;
  world failures hide in the set dressing 20 m back.
- Enforce at two gates: **design review** (before modeling) catches it cheap; **pre-render
  review** (before the farm) catches what slipped. A world error found after render is the
  most expensive error in the pipeline.

## Verify

- [ ] A one-page **charter** exists (place, period, culture/economy, genre/tone) and a
  written **exists / does-not-exist** technology-and-material list for the period.
- [ ] 3–5 **visual motifs** are named, each with a concrete modeler-followable **rule**,
  and their per-sequence presence is tracked.
- [ ] A **scale reference .blend** exists with canonical human height and standard object
  heights; every hero set/prop has been checked against it.
- [ ] An **architecture ruleset** (roof pitch, window proportion, material palette, wall
  module) is written and used.
- [ ] The **consistency bible** holds the asset registry (thumbnail, scale, material IDs,
  shot usage) and is the only accepted source of design truth.
- [ ] Palette/material choices are **keyed to the color-script** per location and
  time-of-day.
- [ ] At least one **location state variant** (e.g. act-1 vs act-3 dressing) is planned
  where the story demands change.
- [ ] A **spot-pause review** of 10 random frames passes the on-world check: no
  anachronism, no wrong-scale object, no off-palette dressing, hero silhouettes distinct.
- [ ] Every proceeding shot traces to a **bible entry**, not a verbal decision.

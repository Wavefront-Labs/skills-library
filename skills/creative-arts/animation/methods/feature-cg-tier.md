---
id: creative-arts.animation.methods.feature-cg-tier
name: feature-cg-tier
category: creative-arts
field: animation
product: methods
tags: [method, recipe, production-method, feature-film, moana, disney, pixar, quality-tier, economics, render-farm, core-hours, labour-bound, compute-bound, feasibility, scoping]
level: advanced
status: draft
description: "Recipe and honest economics for feature-CG (Moana) tier: what it actually costs, and which parts are labour-bound versus compute-bound."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Method: feature-CG tier (Moana / Pixar class) — and when not to attempt it

A **method** is a recipe. This one's main value is **scoping**: it exists so a team
stops re-litigating "why can't we just do Disney quality?" every few weeks. The
answer is arithmetic, and it is worth writing down once.

> Status is `draft`: the economics below are sourced from published production
> figures and from measurement of our own pipeline, but this method has not been
> executed end to end. The *negative* conclusion is the verified part.

---

## The two different walls

Separating these is the whole point. Conflating them produces either despair or
wasted years.

### Labour-bound (agents and automation genuinely help)

Work that decomposes into many independent, checkable tasks:

- texturing and surfacing passes
- set dressing and scatter
- per-shot compositing graphs
- asset cataloguing and licence clearance
- blendshape authoring
- QC sweeps and render babysitting

This is the **bulk** of the gap between blockout and a good stylized series, and it
scales with automation. Do not assume a labour wall where there is none.

### Compute-bound (automation does not help at all)

Feature-CG fidelity is path-traced global illumination with full subsurface, hair
and cloth simulation. Order-of-magnitude: a feature hero frame can consume on the
order of **100 core-hours**, and far more for hair or water shots.

Worked example, one 6.5-minute episode at 24fps:

```
9,360 frames x ~100 core-hours      = ~936,000 core-hours
on a 16-core workstation            = ~58,500 wall-clock hours
                                    = ~6.7 YEARS for ONE episode
```

A studio answers this with a render farm in the tens of thousands of cores. There is
no software trick and no amount of agent parallelism that makes a local GPU render a
path-traced frame faster. **This is the wall.**

### The third wall: iteration count on acting

A feature animator finishes roughly **4 seconds of hand-keyed animation per week**.
A 90-minute feature is ~5,400 seconds, i.e. on the order of **26 animator-years** of
keyframing alone, inside a production of ~800 people over ~5 years.

The deeper problem is not writing the curves — it is that judging whether a
performance *reads* is a perceptual loop requiring a render each time, and hero shots
take dozens to hundreds of iterations. That loop is gated by render time, which puts
it back behind the compute wall.

---

## What this means in practice

1. **Do not target photoreal feature CG on local hardware.** It fails on physics, not
   on skill or effort.
2. **Target a stylization-bound tier instead.** Arcane and Spider-Verse are widely
   held to be more beautiful than photoreal CG, and their quality is **art-direction
   bound** — reachable with craft rather than core-hours. Start at
   `creative-arts.animation.methods.stylized-series-tier`; the climb from there is
   `creative-arts.animation.methods.premium-stylized-tier`, which walks every
   labour-bound rung of the feature list in visibility order and gates the two spots
   where the compute wall creeps back in (sim caching, render budget).
3. **Spend the budget where the eye goes:** faces, compositing, silhouette, motion.
4. **Rejecting the tier is not rejecting the quality.** Nearly every labour-bound
   item on the feature list still applies and still raises the result.

---

## The org chart, mapped (Moana-class crew vs this library)

A WDAS feature credits on the order of **~800 people over ~5 years** for ~90 minutes.
The useful exercise is not awe but a coverage audit: every department is a bundle of
skills, and each bundle either exists in this library or is a named gap. Crew shares
below are order-of-magnitude from published feature credits, to show where the
man-hours actually go.

| Department (approx share of crew) | Library coverage |
|---|---|
| Story & editorial (~5%) | `storywriting.*`, `storyboarding.*`, `editorial.*`, `editing.*` |
| Cultural research / Story Trust (<1%, outsized influence) | `storywriting.cultural-research-authenticity` |
| Vis-dev & art direction (~5%) | `visual-development.*`, `art-direction.*`, `production-design.*`, `character-design.*` |
| Modeling (~7%) | `blender.character-modeling`, `.environment-modeling`, `.organic-sculpting`, `.hard-surface-modeling`, `.sculpt-retopo` |
| Rigging / character TD (~5%) | `blender.rigging`, `.facial-rig`, `.rig-ui-controls`, `.blendshape-sculpting` |
| Look-dev & surfacing (~7%) | `blender.shader-authoring-lookdev`, `.uv-unwrapping`, `texturing.*` |
| Layout / cinematography (~4%) | `blender.layout-blocking`, `.previsualization`, `.camera-cinematography` |
| Animation (~12%; ~4 s/animator/week) | `blender.acting-performance`, `.body-mechanics`, `.animation-blocking-to-polish`, `.graph-editor-polish`, `principles.twelve-principles` |
| Character sim — cloth/hair (~5%) | `blender.cloth-simulation`, `.hair-grooming`, `.hair-simulation` |
| Technical animation / finaling (~4%) | `blender.technical-animation-finaling` |
| FX animation — water was Moana's co-star (~8%) | `blender.fluid-water-fx`, `.smoke-fire-fx`, `.particles-fx`, `.volumetrics-atmospherics`, `.destruction-rbd` |
| Crowds (~2%) | `blender.crowd-animation` |
| Lighting (~12%, often the largest artist dept) | `blender.lighting` |
| Compositing & grade (~4%) | `blender.multipass-compositing`, `.compositing-grade`, `color.color-grading` |
| Rendering & core tech (~8%, Hyperion-class R&D) | `blender.render-optimization`, `.render-aov-passes`, `.rendering-amd-hip` — the R&D itself is the compute wall |
| Pipeline / production engineering (~6%) | `pipeline.pipeline-architecture`, `.asset-management`, `blender.scripting-basics`, `.geometry-nodes`, `.blendercraft-headless` |
| Production management (~5%) | `pipeline.producing-scheduling`, `.production-tracking`, `.dailies-review` |
| Music & songs | `sound-design.scoring`, `.songwriting` |
| Sound design & mix | `sound-design.*` (foley, sfx, ambience, dialogue, final mix) |
| Voice casting & direction | `voice-tts.*`, `voice-direction` |

Reading of the table: **the expertise is coverable; the headcount is not the moat.**
The moat is the two walls above — render R&D plus farm, and the acting-iteration
loop. Everything else on the chart is labour-bound and climbs via
`premium-stylized-tier`. Re-run this audit whenever the library or the ambition
changes; a department with no library row is a gap to write, not to ignore.

---

## If the tier is genuinely required

Then the recipe is organisational, not technical:

- secure render capacity first and size it from a measured core-hours-per-frame
  figure on *your* shots — never from a vendor estimate
- budget the review loop, not just the render: iterations x frames x core-hours
- staff hand-key animation per second of screen time at ~4s/animator/week
- expect bespoke R&D for hair, cloth and water; the open-source solvers are
  approximations, and this is where studio proprietary tech actually lives

## Failure modes

1. **Treating a compute wall as a motivation problem.** Throwing more effort at a
   path-tracing budget produces burnout and no frames.
2. **Treating a labour wall as a compute problem.** Buying hardware when the real
   gap is untextured surfaces and empty frames.
3. **Quoting a tier without measuring your own core-hours per frame.**

## Verify

Before committing to any fidelity target, render ten representative frames at the
proposed settings, measure actual core-hours, and multiply out to the full episode.
If the result exceeds the schedule, the target is wrong — not the team.

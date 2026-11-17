---
id: creative-arts.animation.methods.anime-dialogue-2d-tier
name: anime-dialogue-2d-tier
category: creative-arts
field: animation
product: methods
tags: [method, recipe, production-method, anime, 2d, dialogue, talking-head, consistency, draw-once, puppet, cutout, modern-anime, daima, quality-tier, solo, indie, ordering, gates]
level: advanced
status: verified
description: "Recipe: which skills, in what order, with which gates, to get a drawn 2D character talking at modern-anime quality with zero identity drift, on one machine."
sources: []
licence: Apache-2.0
version: 6
updated: 2026-11-17
aliases: []
---

# Method: 2D anime dialogue tier (drawn characters, one machine)

A **method** is a recipe, not a technique. Every "how" is a link to a skill.

**Outcome:** a lip-synced dialogue shot of a drawn 2D character over a painted plate,
at the appeal of 2020s TV anime, where every frame is provably the same character
because there is exactly one source drawing per character. Executed end to end on a
single AMD workstation: master still → trace → parametric face → 40-drawing talking
test beside a Dragon Ball Daima clip.

**Why this method exists.** A 3D cel-shaded base with outlines, however tuned, was
judged not visually appealing beside Rick and Morty, let alone anime — see the v7
lesson in `creative-arts.animation.methods.stylized-series-tier`. Generation alone
fails the other way: it has appeal but no consistency (four seeds, four characters).
The recipe below takes appeal from generation and consistency from drawing once.

---

## Ingredients

| Phase | Skill |
|---|---|
| Master | `creative-arts.animation.comfyui.anime-character-master-on-amd-directml` |
| Master | `creative-arts.animation.comfyui.dbz-line-and-flat-character-master` |
| Asset | `creative-arts.animation.pipeline.cel-character-from-generated-master` |
| Master | `creative-arts.animation.character-design.model-sheet-turnaround` |
| Face | `creative-arts.animation.character-design.anime-face-construction` |
| Face | `creative-arts.animation.character-design.anime-hair-as-one-mass` |
| Face | `creative-arts.animation.character-design.expression-range-per-character` |
| Asset | `creative-arts.animation.vector-graphics.parametric-features-over-traced-master` |
| Asset | `creative-arts.animation.pipeline.character-consistency` |
| Voice | `creative-arts.animation.pipeline.vo-lipsync-pipeline` |
| Shot | `creative-arts.animation.pipeline.2d-cutout-lipsync-puppet` |
| Shot | `creative-arts.animation.pipeline.cutout-rig-from-flat-character-master` (arms and head on pivots, acting on ones, waist-up MED framing) |
| Shot | `creative-arts.animation.pipeline.2d-shot-renderer-from-masters` |
| Shot | `creative-arts.animation.comfyui.background-master-from-blockout` |
| Shot | `creative-arts.animation.pipeline.2d-character-scene-lighting-pass` |
| Shot | `creative-arts.animation.pipeline.painted-background-plates` |
| QC | `creative-arts.animation.pipeline.episode-qc-cold-viewer` |

## Ordering law
Dependency, not importance: the master fixes the palette and silhouette that the
face must match; the face must exist before the asset split (its line weights have to
survive the mapping scale); the asset must exist before any shot; the plate is
independent and can be made in parallel with everything after the master.

## Phases and gates
1. **Master.** Generate ≥ 4 seeds from one exact prompt; choose one; it is the only
   source from now on. *Gate:* stripe-free at 100 %; owner signs the still.
2. **Face.** Draw the parametric face (front + 3/4) beside a benchmark frame; iterate
   on construction until only polish remains. *Gate:* the 12-variant sheet
   (4 mouths × 3 eyes) reads as one person; upper lid heavier than any other line;
   shadow side and rim light present.
3. **Asset.** Trace, split, map, re-overlay hair. *Gate:* figure beside master is
   identical except at the features; nose and mouth lines visible at the mapped scale.
4. **Shot.** Puppet one real line over a painted master crop, with the scene-lighting
   pass and Daima framing (head ≈ 65 % of frame height). *Gate:* ≥ 10 drawings/s on twos,
   one blink pair, head motion ≤ 12 px, mouth closes before the cut, and a 6-frame
   strip beside the benchmark shows only mouth/eyes/head changing.
5. **QC.** Run the cold-viewer card on the shot; carry the measured rows forward.

## Acceptance criteria
- Identity: pixel-identical hair, clothes and silhouette across all frames of a shot
  and across shots (same trace).
- Appeal: at 640 px beside a Daima/JJK dialogue frame, a cold viewer places the
  character in the same medium (drawn anime), with the remaining gap named as
  lighting/cinematography, not the character.
- Cost: a 3 s line renders in < 1 min CPU; no GPU in the per-frame loop.

## Failure modes this prevents
- Regenerating per shot (identity drift, the owner's "100 % consistency" veto).
- Procedural hair (headband, cutout slabs, saw-blade spikes) — three wasted passes.
- Features too thin to survive the mapping scale (invisible nose).
- A 3D base dressed up with outlines standing in for drawn characters.

## Not covered yet (write the skill, then link it here)
Full-body action (key poses + in-betweens), turns beyond ±20°, hands, and painted
scenery at anime quality. Until those exist, this tier covers dialogue and quiet
acting only.

## Verify
Execute phases 1–4 on a new character in one sitting; if any gate needs more than
three iterations, the skill behind it is missing a lesson — fix the skill, not the
shot.

## Run log
- 22 Oct 2026: traced painted masters judged "not real anime" by the owner against a Dragon Ball
  frame. Rebuilt the cast as line+flat cel masters with blink/mouth replacement cels only; first
  all-2D cut (73 shots, close/medium/wide) reads at 1990s Dragon Ball level beside Daima.
  Still open: head turns (no generated 3/4), hard-edged cel shadow pass, hands, turnarounds.

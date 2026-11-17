---
id: creative-arts.animation.methods.anime-episode-2d-tier
name: anime-episode-2d-tier
category: creative-arts
field: animation
product: methods
tags: [method, recipe, production-method, anime, episode, 2d, series, pipeline, consistency, draw-once, quality-tier, modern-anime, solo, indie, ordering, gates, master-recipe]
level: sme
status: draft
description: "Master recipe: the methods and skills, in order, with gates, to produce a 6–8 minute drawn-2D anime episode on one machine with 100% character and scenery consistency."
sources: []
licence: Apache-2.0
version: 7
updated: 2026-11-17
aliases: []
---

# Method: 2D anime episode tier (master recipe)

A **method** is a recipe, not a technique. This one bundles other methods: it owns
no technique and no gate that a sub-method already owns.

**Outcome:** a 6–8 minute episode in drawn 2D at 2020s TV-anime appeal, where every
character and every location comes from exactly one source drawing, so consistency
is structural, not inspected. Produced by one person plus automation on one
workstation.

**Status: draft.** Phases 1, 3, 4 (all dialogue shots rendered 2D from masters on 21 Oct)
and 7 are verified in production; design-sheet, painted-scenery and action-cut
sub-methods are draft (see each). This file becomes `verified` when one episode has
run through every phase.

---

## Ingredients (methods first, then the skills no sub-method owns)

| Phase | Method / skill |
|---|---|
| Story | `creative-arts.animation.methods.stylized-series-tier` (Story phase only) |
| Story | `creative-arts.animation.storywriting.novel-to-teleplay` |
| Story | `creative-arts.animation.editing.animatic-assembly` |
| Design | `creative-arts.animation.methods.anime-character-design-sheet-tier` |
| Design | `creative-arts.animation.methods.anime-painted-scenery-tier` |
| Voice | `creative-arts.animation.pipeline.vo-lipsync-pipeline` |
| Dialogue | `creative-arts.animation.methods.anime-dialogue-2d-tier` |
| Action | `creative-arts.animation.methods.anime-action-cut-tier` |
| Camera | `creative-arts.animation.blender.camera-cinematography` |
| FX | `creative-arts.animation.blender.compositing-grade` |
| FX | `creative-arts.animation.environment-design.multiplane-and-parallax-layers` |
| Camera | `creative-arts.animation.pipeline.drawn-props-on-cutout-shots` (every object the script names, on screen) |
| Sound + engagement | `creative-arts.animation.methods.anime-engagement-pass-tier` |
| Sound + engagement | `creative-arts.animation.sound-design.shotlist-driven-sfx-and-sting-track` |
| Assembly | `creative-arts.animation.pipeline.2d-shot-renderer-from-masters` |
| Assembly | `creative-arts.animation.pipeline.shot-renderer` (episode cutter, reuse-frames mode) |
| Assembly | `creative-arts.animation.blender.compositing-grade` |
| QC | `creative-arts.animation.pipeline.episode-qc-cold-viewer` |
| QC | `creative-arts.animation.editorial.script-to-picture-audit` |
| QC | `creative-arts.animation.methods.anime-shot-acceptance-and-motion-qa` (acceptance lists, motion strips, independent review, object checks, gate) |
| Design | `creative-arts.animation.methods.reverse-engineer-drawing-style-from-benchmark` (per body part, before production) |
| QC | `creative-arts.animation.sound-design.tts-dialogue-intelligibility-gate` |
| QC | `creative-arts.animation.pipeline.character-consistency` |

## Ordering law
Story locks the shot list, which fixes which locations, angles, expressions and
actions the design packs must contain — so design follows story, not the reverse.
Voice precedes any animation because mouths and accents are timed to it. Dialogue
shots (most of the runtime) are produced before action cuts because they prove the
packs; action cuts are the expensive drawings and should not start on unproven
designs. Camera and FX are applied to finished drawings. The engagement pass (sound
effects, stings, impact frames, pacing) follows camera because it punctuates beats
that must already be on screen. QC runs on every assembly,
not at the end.

## Phases and gates
1. **Story.** Teleplay → shot list → animatic with scratch VO. *Gate:* a cold read of
   the transcript recovers the plot; dialogue density ≥ 0.5× the benchmark.
2. **Design.** Model packs for the cast; master paintings for every location in the
   shot list. *Gate:* the sub-methods' acceptance criteria.
3. **Voice.** Directed VO per line, Rhubarb cues, line fits the shot. *Gate:* no line
   over budget; character floors respected.
4. **Dialogue shots.** Every shot with a line, as 2D puppets over the location
   masters. *Gate:* the dialogue method's gates on every shot, not a sample.
5. **Action cuts.** The beats the script names (chase, stutter, hit). *Gate:* the
   action method's gates.
6. **Camera and FX.** Pushes, pans, parallax, diegetic UI, impact frames, grade.
   *Gate:* cuts per minute and drawings per second within the benchmark band.
7. **Sound and engagement.** Foley and reveal stings from the shot list, impact frames
   on hard hits, cold-open retime, exact silence on the cliff. *Gate:* the engagement
   method's measured checks (stings in sync, sting budget, no line cut).
8. **Assembly and QC.** Concat, mix, cold-viewer card, script-to-picture audit, line
   intelligibility gate. *Gate:* no red rows; every action and spoken reference is on
   screen; every line under 10 % word error rate; side by
   side with the benchmark, the remaining gap is named and smaller than last cut.

## Acceptance criteria
- Every character frame traces to one master; every background frame to one master
  painting.
- Dialogue and action gates met on all shots.
- A cold viewer follows the plot and places the episode in the same medium as the
  benchmark.

## Failure modes this prevents
- Starting animation before the packs exist (every later shot off model).
- Rendering 3D stand-ins "for now" that never get replaced.
- QC only on the final cut.
- A finished-looking cut with no sound effects: viewers read silence as a draft.
- A story told only by the voice track over still characters and one painting per
  location: viewers call the dialogue "broken" even when every word is clear.
- Treating generation as a per-shot art source.

## Verify
Run one episode through phases 1–8, recording each gate; promote this and each draft
sub-method to `verified` as their phases complete.

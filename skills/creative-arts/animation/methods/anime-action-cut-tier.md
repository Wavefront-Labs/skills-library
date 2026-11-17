---
id: creative-arts.animation.methods.anime-action-cut-tier
name: anime-action-cut-tier
category: creative-arts
field: animation
product: methods
tags: [method, recipe, production-method, anime, action, keys, inbetweens, smears, speed-lines, impact-frame, timing, on-twos, dragon-ball, sakuga, 2d, quality-tier]
level: advanced
status: draft
description: "Recipe: skills, order and gates to animate a 2D action beat the anime way — keys and breakdowns, charted in-betweens, smears, speed lines and impact frames, cut on twos with holds."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Method: anime action cut tier

A **method** is a recipe, not a technique. Every "how" is a link to a skill.

**Outcome:** a 1–4 s action beat (run, turn, grab, hit, recoil) drawn pose-to-pose
from the character's model pack, timed on twos with holds, dressed with smears,
speed lines and an impact frame, that reads like a Dragon Ball cut at the
drawing budget of a TV episode (roughly 150–250 drawings per minute of action, far
fewer for dialogue).

**Status: draft.** Timing, holds, blinks and head accents are verified in the
dialogue puppet; full-body keys, in-betweens and effects drawings have not yet been
executed in this pipeline. Frame-interpolation tooling (RIFE-class) is deliberately
NOT an ingredient until a skill exists that verifies it holds a drawn character on
model; until then in-betweens are drawn or charted.

---

## Ingredients

| Phase | Skill |
|---|---|
| Plan | `creative-arts.animation.principles.single-idea-staging` |
| Plan | `creative-arts.animation.principles.shooting-video-reference` |
| Plan | `creative-arts.animation.principles.gesture-drawing-for-animators` |
| Plan | `creative-arts.animation.principles.pose-silhouette-test` |
| Keys | `creative-arts.animation.principles.keys-extremes-breakdowns` |
| Keys | `creative-arts.animation.character-design.line-of-action-in-poses` |
| Keys | `creative-arts.animation.principles.pushing-poses` |
| Keys | `creative-arts.animation.principles.sizing-anticipation` |
| Keys | `creative-arts.animation.principles.anticipation-and-follow-through-staging` |
| Keys | `creative-arts.animation.principles.center-of-gravity-and-balance` |
| Keys | `creative-arts.animation.principles.run-cycle-key-poses` |
| Keys | `creative-arts.animation.principles.landings-and-impact-recovery` |
| Timing | `creative-arts.animation.principles.applying-timing-and-spacing` |
| Timing | `creative-arts.animation.principles.ones-and-twos` |
| Timing | `creative-arts.animation.principles.hold-timing` |
| Timing | `creative-arts.animation.principles.designing-the-breakdown` |
| Timing | `creative-arts.animation.principles.inbetweening-to-charts` |
| Timing | `creative-arts.animation.principles.favouring-inbetweens` |
| Timing | `creative-arts.animation.principles.settles-and-recoil` |
| Effects | `creative-arts.animation.principles.smear-frames-and-multiples` |
| Effects | `creative-arts.comics-and-sequential-art.manga.manga-speed-lines-ryusen` |
| Effects | `creative-arts.comics-and-sequential-art.inking.inking-speed-lines-and-focus-lines` |
| Effects | `creative-arts.animation.principles.squash-and-stretch-in-production` |
| Effects | `creative-arts.animation.principles.secondary-action-hierarchy` |
| Check | `creative-arts.animation.principles.pencil-tests-and-registration` |
| Check | `creative-arts.animation.principles.arc-tracking` |
| Check | `creative-arts.animation.principles.cleanup-line-quality` |
| Check | `creative-arts.animation.art-direction.on-model-checks-across-departments` |

## Ordering law
Staging decides the one idea the cut sells; keys are drawn to that idea from the
model pack; timing is set on the keys (exposure sheet) before any in-between exists,
because in-betweens are the expensive drawings; effects are added last, to the
timed motion, never to disguise weak keys.

## Phases and gates
1. **Plan.** One sentence for what the cut sells; video or mirror reference;
   gesture thumbnails. *Gate:* silhouette test passes on every thumbnail.
2. **Keys.** 3–7 keys + breakdowns, on model, line of action pushed. *Gate:* flip
   the keys alone at 6 fps and the action reads.
3. **Timing.** Exposure sheet on twos with holds; anticipation sized to the action;
   settle after the landing. *Gate:* pencil test of keys + breakdowns at the sheet
   timing reads at full speed.
4. **In-betweens.** Charted (favouring the key they ease toward). *Gate:* arcs
   tracked on the wrist and nose; no pops.
5. **Effects.** Smear on the fastest spacing, speed lines on the frame that carries
   the motion, one impact frame (single-frame high contrast) on the hit. *Gate:* each
   effect is on screen ≤ 3 frames; removing it makes the cut read weaker.
6. **Check.** Registration, line quality, on-model overlay against the pack.

## Acceptance criteria
- Drawings per second: 8–12 on action frames, ≤ 4 on holds.
- Beside a benchmark cut at the same size, a cold viewer names the same action and
  the same hit frame.
- Every drawing overlays its pack view within tolerance.

## Failure modes this prevents
- "Animating" by sliding a cutout (no keys, no anticipation, no settle).
- Interpolated mush between poses that should snap.
- Effects pasted onto static poses.
- Off-model drawings in the fast frames where nobody checks.

## Verify
Execute one 2 s beat (a run-and-stop) end to end; attach the pencil test and the
benchmark comparison; mark `verified` when gates 2–5 hold.

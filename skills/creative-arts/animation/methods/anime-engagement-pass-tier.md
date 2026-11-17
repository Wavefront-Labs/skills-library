---
id: creative-arts.animation.methods.anime-engagement-pass-tier
name: anime-engagement-pass-tier
category: creative-arts
field: animation
product: methods
tags: [method, recipe, production-method, anime, engagement, retention, pacing, cold-open, sting, impact-frame, sfx, cliffhanger, youtube, 2d, quality-tier]
level: advanced
status: draft
description: "Recipe: skills, order and gates for the engagement pass on a 2D episode: cold-open retime, foley, a sting budget, impact frames and an exact cliff silence."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Method: engagement pass (2D anime episode)

A **method** is a recipe, not a technique. It bundles skills in order with gates.

**Outcome:** a picture-locked episode stops feeling like a draft and starts paying the
viewer off on a rhythm. Hits are heard and seen, the opening moves, and the ending
lands in silence. It runs after camera and FX and before final assembly QC, inside
`anime-episode-2d-tier`.

**Status: draft.** Steps 1 to 5 ran on one 6-minute episode (one production cut)
with every check below measured on the final cut.

## Ingredients

| Step | Skill |
|---|---|
| Audit | `creative-arts.animation.pipeline.episode-qc-cold-viewer` |
| Retime | `creative-arts.animation.pipeline.2d-shot-renderer-from-masters` (re-trim, reuse frames) |
| Foley + stings | `creative-arts.animation.sound-design.shotlist-driven-sfx-and-sting-track` |
| Sound choice | `creative-arts.animation.sound-design.foley-design`, `creative-arts.animation.sound-design.cartoon-sfx-vocabulary` |
| Impact frames | `creative-arts.animation.methods.anime-action-cut-tier` (impact frame) + the ffmpeg recipe in the sfx skill |
| Mix | `creative-arts.animation.sound-design.final-mix` |

## Order and why

1. **Audit the script before touching the cut.** Check whether the episode already
   opens cold before the title and ends on a cliff. If it does, do not reorder the
   story; the gains are in timing and punctuation. Reordering a writer's script is an
   owner decision.
2. **Retime the cold open.** Dialogue shots go to voice-over length plus 0.5 s, never
   longer than before, with a 2 s floor. Silent beats go to 2 to 2.5 s, except one
   deliberate hold before the title. *Gate:* no line is cut; the cold open is shorter.
3. **Mark the beats in the shot list.** Add `sting` and `impact` times to the reveal
   and hit shots. *Gate:* about one sting per 40 s of runtime, and impact frames only
   on hard physical or reveal hits.
4. **Build foley and stings, synced to measured clip starts.** *Gate:* envelope
   cross-correlation between mix and effects track gives zero lag at several points.
5. **Impact frames and the cliff.** One inverted drawing plus a decaying shake on
   the hit shots. Dead silence from the first sample of the smash to black.
   *Gate:* the inverted frame sits on the hit in a frame tile from the final cut;
   RMS in 0.2 s windows reads digital silence across the black.
6. **Look for what the punctuation exposes.** An impact frame on a shot that does not
   show the event (a bag split with no bag) is now loud. List each one as a prop or
   pose fix for the next cut.

## Acceptance criteria

- Every scripted sound cue in the shot list has a sound on the cut.
- Stings sit clearly over the bed (measured about 9 dB) and stay within the budget.
- The cold open is tighter with every line intact.
- Silence on the cliff is exact, and audio length matches picture.

## Failure modes this prevents

- A cut with voice and music but no effects, which viewers read as unfinished.
- Stings drifting off picture late in the episode because timing was summed, not
  measured.
- Stinging every beat until none of them land.
- Reordering the story when the gap was pacing.

## Verify

Run steps 1 to 6 on one episode and record each gate. Promote to `verified` after a
second episode passes without changes to the recipe.

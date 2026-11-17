---
id: creative-arts.game-design.narrative-design.cutscene-design
name: cutscene-design
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, cutscene-design, cinematics, in-engine-cinematics, skippable-cutscenes, narrative-delivery]
level: practitioner
status: draft
description: "Design cutscenes that respect play: when to take control, length, skip rules, gameplay-to-cinematic transitions, camera grammar and checkpointing around cinematics."
sources:
  - https://dev.epicgames.com/documentation/en-us/unreal-engine
  - https://gameaccessibilityguidelines.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cutscene design

**Goal:** cinematics that deliver what play cannot, without stealing the player's moments
or punishing retries.

## When to use a cutscene
- **Use** for: establishing a new place or character, time skips, events the player
  cannot be present for, emotional close-ups that need authored framing.
- **Do not use** for: the player's own heroic action (let them perform it), information
  needed to play (they will skip it), anything that could be a playable scripted moment.

## Types
| Type | Notes |
|---|---|
| Pre-rendered video | highest fidelity; costumes and gear mismatch the player's |
| In-engine real-time | matches gear and lighting; built in Sequencer (Unreal) or Timeline (Unity) |
| Interactive / QTE | keeps hands busy; failure states need design |
| Walk-and-talk / playable cinematic | player keeps control, camera and pacing are guided |

## Rules
1. **Length:** most under 2 minutes; break longer ones with interaction.
2. **Skip:** every cutscene skippable, with a hold-to-skip or confirm to avoid accidental
   skips; pause must be possible. Offer a scene recap or log entry for skipped info.
3. **Checkpoint after**, not before, a cutscene that precedes a boss, so retries do not replay it.
4. **Transitions:** blend from the gameplay camera into the first shot and back out to a
   gameplay-ready camera facing the next objective. Return control with the character idle,
   not mid-animation.
5. **Camera grammar:** keep the 180-degree rule in dialogue, establish geography with a
   wide, cut on action. Letterbox signals "no control" to players.
6. **Subtitles and speaker names** on by default, with size options.

## Pipeline
Storyboard / animatic -> blockout in engine with placeholder VO -> mocap and final VO ->
lighting pass -> audio mix. Lock the script before mocap.

## Gotchas
- Cutscenes where the player character does something the player would not choose damage
  identification; foreshadow it or make it a choice.
- In-engine scenes must handle any equipped gear and companion state; test extremes.
- Loading hidden behind cutscenes still needs a fallback when the skip is faster than the load.

## Verify
- [ ] Every cutscene skippable and pausable.
- [ ] Checkpoints placed after pre-boss cinematics.
- [ ] Control returns facing the next objective.

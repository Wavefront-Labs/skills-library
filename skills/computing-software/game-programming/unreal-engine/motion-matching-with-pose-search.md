---
id: computing-software.game-programming.unreal-engine.motion-matching-with-pose-search
name: motion-matching-with-pose-search
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, unreal-animation, motion-matching, pose-search, chooser-tables, game-programming]
level: practitioner
status: draft
description: "Set up Unreal 5 motion matching with the Pose Search plugin: schemas, databases, trajectory from CharacterMovement, Motion Matching node, and debugging with the Rewind Debugger."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-matching-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/game-animation-sample-project-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Motion matching with Pose Search

**Goal:** locomotion driven by searching an animation database for the pose and trajectory that
best fit the current state, instead of hand-built state machines.

## Assets
- Enable **Pose Search** (and for trajectory helpers, **Animation Warping**, **Chooser**).
- **Pose Search Schema**: skeleton, sample rate, channels — Trajectory (past/future sample times,
  position/velocity/facing), Pose (bones like feet and pelvis, velocity/position), Heading.
- **Pose Search Database**: list of animation sequences/blend spaces using the schema; tags and
  per-animation settings (looping, mirroring, sampling range).
- Optional **Pose Search Normalization Set** to balance channels across databases.

## Runtime
- Generate a trajectory from CharacterMovement each frame (UE 5.4+: `PoseSearchTrajectoryLibrary`
  / Character Trajectory component; 5.5+ trajectory functions in the anim instance). Future samples
  predict from velocity/acceleration and input.
- Anim graph: **Motion Matching** node with the databases (or a Chooser Table selecting databases by
  state — idle/moving/jumping, stance).
- Set Blend Time, Pose Jump Threshold Time, Search Throttle. Use **Orientation/Stride Warping** after it
  to fix foot sliding when capsule speed differs from animation speed.

## Debugging
Rewind Debugger (Tools > Debug > Rewind Debugger): record PIE, scrub, and inspect the Pose Search
track — chosen database/asset, cost breakdown by channel, and competing candidates. Look for a channel
dominating cost (normalise or weight it).

## Data quality
- Dance cards / mocap with starts, stops, pivots at multiple angles and speeds; gaps in coverage show
  as foot sliding or poor responsiveness.
- Mirror animations via a Mirror Data Table to double coverage.

## Gotchas
- Root motion vs capsule-driven movement: Game Animation Sample uses capsule-driven movement with
  warping; mixing root motion requires care.
- Schema change invalidates database indexes (rebuild; DDC caches the index).
- Large databases cost CPU per search; throttle searches and use KD-tree/VPTree settings.

## Verify
- [ ] Rewind Debugger shows low-cost picks with smooth asset transitions in pivots and stops.
- [ ] Foot sliding visibly reduced with warping enabled.

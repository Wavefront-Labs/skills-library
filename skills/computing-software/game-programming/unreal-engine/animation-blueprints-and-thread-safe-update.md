---
id: computing-software.game-programming.unreal-engine.animation-blueprints-and-thread-safe-update
name: animation-blueprints-and-thread-safe-update
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-animation, animation-blueprint, anim-instance, thread-safe-update, blueprintthreadsafeupdateanimation, property-access, fast-path, anim-graph, game-programming]
level: practitioner
status: docs-checked
description: "Write performant Unreal Animation Blueprints: Thread Safe Update Animation, thread-safe functions, Property Access, Animation Fast Path, node functions and URO, per Epic."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprints-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/graphing-in-animation-blueprints-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-optimization-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Animation Blueprints and thread-safe update

**Goal:** keep character animation logic off the game thread where possible.

## Two graphs
- **EventGraph** runs on the game thread, together with most other Blueprint logic. Epic recommends using it as little
  as possible; the Animation Optimization page calls its logic generally the most expensive part of an Animation
  Blueprint.
- **AnimGraph** executes on a separate worker thread by default. Safe operations include most AnimGraph nodes,
  direct member-variable access (including struct members) and pure functions that do not modify state. The compiler
  warns about unsafe operations. Turning off **Use Multi Threaded Animation Update** (Class Settings) runs it on the
  game thread; Epic does not recommend that.

## Thread-safe update
1. In My Blueprint, Override dropdown (Functions category) > **Blueprint Thread Safe Update Animation**. It has a Delta
   Time pin and runs on the worker thread; the EventGraph Update Animation event always runs on the game thread.
2. Make helper functions thread safe: new function in My Blueprint, Details panel, enable **Thread Safe**; then call
   them from the override. Disabling Thread Safe on a function moves it to the game thread (not recommended).
3. Thread-safe functions cannot directly touch non-thread-safe Blueprints and components: use **Property Access**
   (right-click in the thread-safe function graph, or in the AnimGraph Variables category > Property Access, or on a
   node pin's dropdown). Bind through the Bind dropdown, e.g. a Get chain such as `TryGetPawnOwner` then
   `GetActorLocation` (the Graphing page's example). Custom property-access functions need a Return Node feeding a
   `ReturnValue` pin and **Pure** enabled.
4. The page says data from other Blueprints must be called (pulled) by the Animation Blueprint rather than pushed to it.
5. Property Access **Call Site** options: Automatic (leave it in most cases), Thread Safe, Game Thread or Worker Thread
   each Pre- or Post-Event Graph.

## Animation Fast Path
Lets the engine copy parameters internally instead of calling into the Blueprint VM. Optimisable constructs: member
variables, negated boolean member variables, members of a nested structure (Split Struct Pin or a Break node; Break
Transform does not qualify). Any calculation on the pin (the page's example is a multiply) loses it; fast-path nodes
show a lightning icon. Enable **Warn About Blueprint Usage** under Optimization in the Anim Blueprint's Class Settings
to get Compiler Results warnings for non-fast-path access.

## Node functions
Animation node Details > Functions: On Initial Update (once, first time the node becomes relevant), On Become Relevant
(every time it becomes relevant again), On Update (every tick while relevant). Relevant means contributing to the
Output Pose. Add one with the dropdown > Create Binding. Pins: Context and Node.

## General tips (Animation Optimization page)
- Parallel update conditions are in `UAnimInstance::NeedsImmediateUpdate`; needing root motion for character movement
  prevents parallel update.
- URO (Skeletal Mesh Component > Optimization > Enable Update Rate Optimizations; `AnimUpdateRateTick()` struct; Display
  Debug Update Rate Optimizations for an on-screen view). Epic suggests targeting 15Hz and under at suitable
  distances with interpolation disabled, and says the Animation Budget Allocator plugin is recommended over URO.
- Enable Component Use Fixed Skel Bounds when the character does not need its Physics Asset.
- Rewind Debugger records PIE segments for animation analysis; Animation Insights may show
  `FParallelAnimationCompletionTask` on the main thread.

## Checked
Date: 2026-11-07. Read in full: Animation Blueprints (creation, assigning), Graphing in Animation Blueprints (all
sections) and Animation Optimization (all sections), unversioned en-us pages that state no engine version.
Removed as not on those pages: the C++ `UAnimInstance` class (`NativeThreadSafeUpdateAnimation`), the "Allow Multi
Threaded Animation Update" Project Settings entry (the page names the Class Settings option Use Multi Threaded
Animation Update), Lyra attribution, `VisibilityBasedAnimTickOption`, `a.ParallelAnimUpdate 0`, the Automatic Rule
Based transition advice, Linked Anim Layers advice, the Debug object dropdown, and the Verify checklist (including "50
characters" budget).
Method: documentation only; no commands were run.

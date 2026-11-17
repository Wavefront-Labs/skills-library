---
id: computing-software.game-programming.game-ai-programming.event-driven-behaviour-trees
name: event-driven-behaviour-trees
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, event-driven-behavior-tree, behaviour-trees, observer-aborts, game-programming]
level: practitioner
status: draft
description: "Make behaviour trees event-driven: only tick running nodes, re-evaluate conditions on blackboard change, observer aborts and when full ticking is simpler."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-tree-in-unreal-engine---overview", "https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter06_The_Behavior_Tree_Starter_Kit.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Event-driven behaviour trees

**Goal:** stop re-evaluating the whole tree from the root every frame for every agent, while still
reacting immediately when conditions change.

## Full ticking (classic)
Each tick evaluates from the root; simple and reactive, but cost scales with tree size and agent
count, and every condition runs constantly.

## Event-driven (Unreal style, Champandard and Dunstan's *Behavior Tree Starter Kit*)
- Keep the currently running path; each tick only updates the running leaf task.
- Conditions become **decorators observing blackboard keys**. When an observed key changes, the
  decorator re-checks and, if its result flipped, triggers an abort.
- Unreal decorator "Observer aborts": `Self` (abort this subtree when condition fails), `Lower
  Priority` (abort running lower-priority branches when this higher-priority condition becomes
  true), `Both`.
- After an abort, execution restarts the search from the aborting point.

## Implementation sketch
```cpp
blackboard.onChanged(key, [this](Key k) {
    for (Decorator* d : observers[k]) if (d->isRelevant() && d->evaluate() != d->lastResult) requestAbort(d);
});
```
Process abort requests at a safe point in the tick (not inside the blackboard setter).

## Pitfalls
- Conditions that depend on non-blackboard state (distance to target changing continuously) never
  trigger; push them into the blackboard via services at intervals or make them polled.
- Abort storms when a key oscillates; add hysteresis in the service that writes it.
- Tasks must handle abort cleanly (stop movement, release smart objects).

## When not to bother
Small trees and few agents: full ticking is easier to reason about and fast enough.

## Verify
- Profiler: BT cost per agent drops; test that a higher-priority branch interrupts within one tick
  of its key changing.

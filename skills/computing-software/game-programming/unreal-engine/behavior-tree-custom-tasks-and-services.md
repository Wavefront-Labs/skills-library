---
id: computing-software.game-programming.unreal-engine.behavior-tree-custom-tasks-and-services
name: behavior-tree-custom-tasks-and-services
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-ai, unreal-behavior-tree, bt-task-node, unreal-bt-task, btservice, btdecorator, blackboard, observer-aborts, aicontroller, game-programming]
level: practitioner
status: docs-checked
description: "Unreal Behavior Tree concepts and Blueprint tasks: event-driven execution, Blackboard, Decorators, Services, Simple Parallel, Observer Aborts, AI Controller and Execute AI events."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-tree-in-unreal-engine---overview", "https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-tree-in-unreal-engine---quick-start-guide"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Behavior Tree custom tasks and services

**Goal:** Unreal AI built from small reusable task and service nodes that react to Blackboard changes instead of polling.

## Concepts (Behavior Tree Overview page)
- A Behavior Tree holds logic; a separate **Blackboard** asset stores the Blackboard Keys it needs. Execution runs left
  to right, top to bottom, with order numbers in the nodes' upper-right corner.
- Decorators (conditionals) attach to Composite nodes; purple nodes are Task nodes (actions).
- A Pawn has an AI Controller that runs the tree when it possesses the Pawn; navigation needs a NavMeshBoundsVolume in the
  Level.
- **Event-driven**: the tree listens for events rather than re-checking each tick, which Epic says improves performance
  and debugging; a Blackboard Key change can abort lower-priority Tasks.
- Epic recommends Decorators rather than Task leaf nodes for conditionals.
- **Simple Parallel** has two children: one single Task (optional Decorators) and one complete sub-tree: "While doing A,
  do B as well."
- **Services** attach to Composite nodes (Selector, Sequence, Simple Parallel) and register for callbacks every set
  number of seconds; active while execution stays in that Composite's sub-tree (e.g. choosing the best enemy to pursue).
  The Quick Start also says Services attach to Task nodes and take the place of traditional Parallel nodes.
- **Observer Aborts** on a Decorator replace "check the condition in a parallel branch": the page's example is a "Mouse Can
  Be Pounced On?" Decorator on the Sequence with Observer Aborts = `Self`.

## Blueprint task and service events (Quick Start page)
- Custom Task Blueprint (e.g. `BTT_ChasePlayer`): add Event Receive Execute AI, finish with a Finish Execute node (Success
  flag). Use the AI variants of Event Receive Execute, Abort and Tick when the agent is an AI Controller; if both generic
  and AI versions are implemented only the more suitable one is called.
- Custom Service: use Event Receive Activation AI; no Finish Execute node is needed.
- Run the tree from the AI Controller: on possession (Event On Possess) call **Run Behavior Tree** with `BTAsset`; it
  targets AI Controller Blueprint classes.
- If the AI is spawned after the world loads, set Auto Possess AI to Spawned.
- Wait task: Wait Time 4.0 with Random Deviation 1.0 waits 3 to 5 seconds.
- Blackboard Decorator (Blackboard Based Condition) with Observer Aborts = `Both` and key `HasLineOfSight`: when the
  value changes it aborts itself (the Chase Player branch) and lower-priority tasks, and when it becomes set it aborts
  lower-priority tasks so the chase branch can run.

## Checked
Date: 2026-11-07. Read in full: Behavior Tree Overview page (all sections). Quick Start page read by targeted search
of the whole text plus lines 270-304 (the Decorator, Services and On Your Own sections); the step-by-step Blueprint
tutorial sections 1-6 were not read line by line. Unversioned en-us pages, no engine version stated.
Removed: the entire C++ `UBTTaskNode` example (`ExecuteTask`, `TickTask`, node memory, `FinishLatentTask`,
`GetInstanceMemorySize`, `bCreateNodeInstance`), Build.cs module list, `RunBehaviorTree` C++ call, `UBTService`
`TickNode`/Interval, `CalculateRawConditionValue`, the `Lower Priority` and `Both` definitions beyond what the Quick Start
states, Gameplay Debugger key and category, `UE_VLOG`/Visual Logger menu path, and the Verify checklist. The node-reference
source URL returns empty text and was dropped from `sources`.
Method: documentation only; no commands were run.

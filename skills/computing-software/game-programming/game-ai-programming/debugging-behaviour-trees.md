---
id: computing-software.game-programming.game-ai-programming.debugging-behaviour-trees
name: debugging-behaviour-trees
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, bt-debugging, behaviour-trees, ai-debugging, game-programming]
level: practitioner
status: draft
description: "Debug behaviour trees: live tree visualisation with node status, execution history, blackboard inspection, breakpoints and logging why a branch failed."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-tree-in-unreal-engine---user-guide", "https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter06_The_Behavior_Tree_Starter_Kit.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debugging and visualising behaviour trees

**Goal:** answer "why is this NPC doing that?" in seconds.

## Live visualisation
- Draw the tree for the selected agent with each node coloured by last status this tick:
  running (yellow), success (green), failure (red), not evaluated (grey). Unreal's Behavior Tree
  editor does this during PIE when an AI is selected; replicate it in your own ImGui overlay.
- Show the active path from root to running leaf in world-space text above the agent.

## Execution history
Record per tick: nodes entered, results, aborts and which decorator caused them, into a ring buffer
per agent. Allow scrubbing back (Unreal's Visual Logger `UE_VLOG` records AI state with a timeline
and gameplay debugger categories; Unreal BT debugger supports stepping back through history).

## Blackboard
Display all keys with values and the frame they last changed; flag keys read but never set
(misspelt key names are a classic bug). Typed keys and asserts on missing keys prevent silent defaults.

## Explaining failures
Decorators and conditions should log a reason string when they fail in debug builds
("HasLineOfSight: blocked by Crate_12"). Aggregate: which node fails most per agent type.

## Breakpoints
Node-level breakpoints that pause the game when a node starts or fails for the selected agent.

## Common bug patterns
- Selector stuck on a running low-priority branch because higher priorities aren't re-evaluated:
  missing observer aborts or a non-reactive tree.
- Tasks returning success instantly when they should run (moving 0 m because target was null).
- Services updating blackboard values too slowly (tick interval).

## Verify
- Reproduce a bug from QA using recorded history alone, without a debugger attached.

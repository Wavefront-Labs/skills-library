---
id: computing-software.game-programming.gameplay-programming.generative-grammars-for-levels
name: generative-grammars-for-levels
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, generative-grammar, mission-generation, procedural-generation, game-programming]
level: practitioner
status: draft
description: "Generate missions and levels with generative grammars: graph rewriting for lock-and-key missions, then mapping mission graphs to space."
sources: ["https://tracery.io/", "https://www.boristhebrave.com/2021/04/10/dungeon-generation-in-unexplored/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generative grammars for missions and levels

**Goal:** structured procedural content (locked doors before keys, a boss at the end) that pure
noise or random rooms cannot guarantee. Based on Joris Dormans' mission/space grammars, used in
*Unexplored*.

## Two layers
1. **Mission graph:** abstract nodes (start, key, lock, challenge, boss, goal) and edges (must come before).
2. **Space:** rooms and corridors realising the mission graph.

## Graph rewriting rules
```text
rule add_lock_key:   A -> B        becomes   A -> Key -> ... -> Lock -> B   (key reachable before lock)
rule add_challenge:  A -> B        becomes   A -> Challenge -> B
rule branch:         A -> B        becomes   A -> B, A -> Side -> Reward
```
Apply rules with weights and limits from a start graph `Start -> Goal` until a size budget is hit.
Because rules preserve ordering edges, every generated mission is solvable by construction.

## Mapping to space
- Embed graph nodes on a grid or into prefab rooms; lock nodes become doors; keys placed in rooms
  reachable without crossing their lock.
- *Unexplored* uses cyclic generation: rules insert cycles (two paths between nodes) for
  backtracking loops rather than trees.

## Validation
Even with correct rules, run a solver: BFS over (room, keys held) state to confirm the goal is
reachable and every key is obtainable. Reject and regenerate on failure, logging the seed.

## Tools
Grammar engines: Dormans' Ludoscope, or a hand-rolled subgraph matcher (fine for under 100 nodes).
Text grammars (Tracery) suit quest names and descriptions.

## Verify
- Generate 10,000 seeds; solver success 100%, distribution of lengths within budget.

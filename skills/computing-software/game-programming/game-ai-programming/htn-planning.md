---
id: computing-software.game-programming.game-ai-programming.htn-planning
name: htn-planning
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, htn-planning, hierarchical-task-network, compound-task, primitive-task, methods, planner, replanning, utility-ai, goap, game-programming]
level: advanced
status: verified
description: "Build an HTN planner for NPCs: world state, primitive and compound tasks with ordered methods, forward decomposition, plan execution, and replanning on world changes."
sources: ["https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter12_Exploring_HTN_Planners_through_Example.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTN planning

**Goal:** NPCs that build multi-step plans from designer-authored recipes ("to attack: get in
range, then fire; if no ammo: reload first"), more controllable than GOAP and less brittle than
hand-written state machines (Humphreys, Game AI Pro ch. 12; Transformers: Fall of Cybertron).

## Concepts
- **World state**: a small fixed array of facts (enums/ints/bools) the planner can copy cheaply.
- **Primitive task**: an executable action with preconditions, effects (applied to the planning
  copy) and an operator (runtime code).
- **Compound task**: a goal decomposed by an **ordered list of methods**; each method has
  conditions and a subtask list. The first method whose conditions hold is used.
- **Root task**: the top compound task (e.g. `BeEnemy`).

## Domain example
```
Compound BeEnemy
  method [EnemyVisible]        -> [AttackEnemy]
  method [HeardNoise]          -> [Investigate]
  method []                    -> [Patrol]
Compound AttackEnemy
  method [Ammo == 0]           -> [NavigateToCover, Reload, AttackEnemy]
  method [DistanceToEnemy > 20]-> [NavigateToEnemyRange, FireWeapon]
  method []                    -> [FireWeapon]
Primitive FireWeapon  pre: Ammo > 0   effect: Ammo -= 1
Primitive Reload      pre: none       effect: Ammo = MagSize
```

## Planner (forward decomposition, depth-first with backtracking)
```
plan(root, state):
  tasks = [root]; plan = []; ws = copy(state); history = []
  while tasks not empty:
    t = tasks.pop_front()
    if t is compound:
      m = first method of t (starting after any previously failed index) whose conditions hold in ws
      if m: history.push(snapshot(tasks, plan, ws, t, m.index)); tasks = m.subtasks + tasks
      else: restore last history entry and try its next method (backtrack); fail if none
    else:
      if t.preconditions(ws): t.apply_effects(ws); plan.push(t)
      else: backtrack
  return plan
```
Methods' order = designer priority. No heuristic search is needed, so it is fast and predictable.

## Execution and replanning
- Execute primitive tasks in order; each operator returns Running/Succeeded/Failed.
- Before executing each task, re-check its preconditions against the **real** world state; fail ->
  replan.
- Replan on significant world-state changes (new enemy, damage) but compare the new plan's
  **method traversal record** (which method indices were chosen) with the current one and switch only
  if the new plan is higher priority; avoids plan thrashing.
- Expected effects (effects applied during planning but only guaranteed at runtime) need care.

## HTN vs GOAP vs BT
HTN: designer-ordered decomposition, cheap, predictable. GOAP: searches action combos to satisfy a
goal, more emergent, harder to control. BTs: reactive with no lookahead. HTN suits squad/tactical AI
needing lookahead with designer control.

## Verify
- [ ] Unit tests: given world states produce expected plans (golden plans per scenario).
- [ ] Debug UI shows current plan, active task and method traversal record.
- [ ] Replanning frequency under combat stays bounded (no thrashing between equal-priority plans).

## Checked (2026-10-22)
- Implemented the planner (decompose first applicable method, history stack, backtrack to the next method) for the Domain example: Ammo 0 and enemy visible gives `NavigateToCover, Reload, FireWeapon`; Ammo 3 and distance 30 gives `NavigateToEnemyRange, FireWeapon`; no visible enemy gives `Patrol`. The recursive `AttackEnemy` after `Reload` resolves because conditions are evaluated against the planning copy of the state.
- Game AI Pro ch. 12 PDF: Troy Humphreys, Transformers: Fall of Cybertron, method traversal record (MTR), decomposition history and restore. Removed the Killzone 2 mention and the GDC Vault link, which could not be fetched (HTTP redirect to a maintenance page).

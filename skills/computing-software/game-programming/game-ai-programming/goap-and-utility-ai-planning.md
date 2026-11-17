---
id: computing-software.game-programming.game-ai-programming.goap-and-utility-ai-planning
name: goap-and-utility-ai-planning
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, goap, goal-oriented-action-planning, utility-ai, scoring, response-curves, considerations, a-star-planner, preconditions, effects, world-state, fsm-alternative, behaviour-tree-alternative, the-sims, fear, game-programming, utility-considerations]
level: advanced
status: draft
description: "Choose between GOAP (planning a sequence of actions toward a goal) and utility AI (scoring which single action to take now), and know their real failure modes."
sources: ["https://www.gdcvault.com/play/1012410/Improving-AI-Decision-Modeling-Through"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# GOAP and utility AI planning

**Goal:** pick the right decision architecture for NPC behaviour beyond a
behaviour tree's hand-authored branches — GOAP when the *order* of actions
matters and should emerge rather than be scripted, utility AI when you need one
best action chosen from many competing concerns every tick.

## GOAP: planning, not scripting
GOAP (Goal-Oriented Action Planning, from F.E.A.R.) gives an agent a set of
**Actions**, each with preconditions and effects expressed as world-state facts
(`HasWeapon: true`, `EnemyVisible: true` → `EnemyDead: true`), a **current world
state**, and a **Goal** (`EnemyDead: true`). A planner (commonly A* over the
space of world-states, treating each Action as an edge with a cost) searches for
a sequence of Actions whose chained effects reach the goal from the current
state — `GoTo(weapon) → PickUp(weapon) → GoTo(enemy) → Attack(enemy)` — without
anyone having hand-authored that specific chain. Add a new Action (say,
`Reload`) and the planner can incorporate it into plans no designer explicitly
wrote.
- **Cost of this power**: debugging *why* a plan wasn't found is harder than
  debugging a behaviour tree, because the failure is "no sequence of actions
  satisfies the goal from this state" rather than a specific branch not firing.
  Log the planner's rejected-state frontier when things go wrong, not just the
  final plan.
- **Replan on world-state change** (an action's precondition becomes false mid-
  execution — the picked-up weapon got destroyed) — don't execute a stale plan
  blindly; check preconditions before each step or replan on any relevant world
  event.
- GOAP shines for "what sequence gets me there" (one agent, several steps). It's
  the wrong tool for "which single reaction now" — that's utility AI.

## Utility AI: scoring, not sequencing
Utility AI evaluates every candidate action **this tick** by scoring it from
several weighted **considerations** (0..1 each, e.g. `DistanceToTarget`,
`MyHealthPercent`, `AmmoRemaining`), combining them (commonly multiplicatively,
so any consideration near 0 vetoes the action) into one utility score per
action, then picks the max. This naturally blends competing drives ("should I
flee, heal, or attack?") without an explicit decision tree enumerating every
combination — the classic example from The Sims is NPCs balancing Hunger,
Energy, Fun simultaneously.
- Each consideration is usually a **response curve** (linear, exponential,
  logistic) mapping a raw value (health 0-100) to a 0..1 score — tune the curve
  shape, not just a weight, since a linear "flee if health < 50%" feels
  different from a curve that ramps sharply only below 20%.
- **Failure mode: oscillation.** Two actions near-tied in score flip-flop every
  frame (attack ↔ retreat) when the inputs change slightly. Fix with hysteresis
  — require a challenger to beat the current action's score by a margin, or add
  a minimum-commitment timer before an action can be re-evaluated.
- Utility AI answers "what to do right now" well; it has no native notion of
  multi-step sequencing — pair it with a simple FSM per chosen action, or GOAP
  underneath the chosen high-level action, if execution needs several steps.

## Combining with behaviour trees
Many shipped AAA systems use a **hybrid**: a behaviour tree or utility selector
picks the current high-level goal, and a GOAP planner or an FSM handles
execution of that goal's steps. Don't treat these as mutually exclusive with
`computing-software.game-programming.game-ai-programming.astar-pathfinding-and-behaviour-trees`
— planning/utility decide *what*, behaviour trees/FSMs often still execute
*how*.

## Verify
- [ ] GOAP actions' preconditions/effects cover the real failure case ("no plan
      found") with a diagnosable log, not a silent idle NPC.
- [ ] Utility scores use normalized 0..1 considerations with explicit response
      curves, not raw unnormalized magnitudes multiplied together.
- [ ] Tie-breaking/hysteresis tested by nudging an input slowly across a
      decision boundary — no visible flicker between two actions.
- [ ] Replanning/rescoring frequency is budgeted (not every agent every frame)
      and verified against the agent count target in the Profiler.

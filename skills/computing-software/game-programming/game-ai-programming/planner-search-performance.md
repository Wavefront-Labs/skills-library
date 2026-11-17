---
id: computing-software.game-programming.game-ai-programming.planner-search-performance
name: planner-search-performance
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, planner-optimization, goap, htn, game-programming]
level: practitioner
status: draft
description: "Speed up GOAP and HTN planners: regressive search, compact world-state bitsets, heuristics, plan caching, replanning triggers and per-frame budgets."
sources: ["https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter12_Exploring_HTN_Planners_through_Example.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Planner search performance

**Goal:** GOAP and HTN planners that stay within an AI frame budget with dozens of agents.

## World state representation
Use a fixed set of symbols packed into bitsets or small arrays: `uint64_t values, mask` (which
bits are set/care). Precondition check = `(state & pre.mask) == pre.values`; applying effects is two
bit operations. Strings or maps in the inner loop are the usual reason planners are slow.

## Search choices (GOAP)
- **Regressive search** from the goal (F.E.A.R. used it): only actions whose effects satisfy unmet
  goal conditions are considered, a much smaller branching factor than forward search.
- A* with heuristic = number of unsatisfied conditions (admissible if each action fixes at most one
  condition; otherwise scale down).
- Cap plan depth (4-6 actions) and nodes expanded per search.
- Precompute effect -> actions lookup tables.

## HTN
Total-order forward decomposition (SHOP-style) is usually fast because methods prune heavily; keep
method preconditions cheap and ordered most-likely first. Partial replanning: re-decompose only from
the failed task.

## Reuse and replanning
- Cache plans per (goal, relevant state hash) for agent archetypes; validate before use.
- Replan only on triggers: plan step failed, relevant world state changed, higher-priority goal
  became valid. Not every frame.
- Context checks (procedural preconditions like "is path reachable") are expensive; run them after
  cheap symbolic checks and cache results per planning call.

## Budgeting
Queue planning requests and time-slice across frames; agents keep executing current plans or idle
animations while waiting.

## Verify
- Profile nodes expanded and microseconds per plan; stress with 50 agents replanning simultaneously.

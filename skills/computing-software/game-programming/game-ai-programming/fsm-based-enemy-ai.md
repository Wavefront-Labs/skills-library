---
id: computing-software.game-programming.game-ai-programming.fsm-based-enemy-ai
name: fsm-based-enemy-ai
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, enemy-ai-fsm, finite-state-machine, enemy-ai, game-programming]
level: practitioner
status: draft
description: "Build enemy AI with finite state machines: patrol, investigate, chase, attack and search states, transition conditions, alert levels and avoiding state thrashing."
sources: ["https://gameprogrammingpatterns.com/state.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FSM-based enemy AI

**Goal:** readable, predictable enemy behaviour from a small state machine, the backbone of most
action-game enemies.

## Typical states
```text
Idle/Patrol --(sees player)--> Alert --(confirms)--> Chase --(in range)--> Attack
     ^                           |                    |  ^                    |
     |                     (lost, timeout)       (lost sight)          (out of range)
     +------ Return <---- Search <----------------+  +--------------------+
Any --(health <= 0)--> Dead          Any --(heavy hit)--> Stagger (returns to previous)
```
- **Alert/Investigate** state gives players a readable warning before full aggression (stealth games
  use suspicion meters filling over time based on visibility).
- **Search** goes to last known position, then checks nearby points before giving up.

## Implementation
State objects with `enter/update/exit` and a transition check per update; centralise transitions in
a table or in each state's update returning the next state. Keep perception separate: states read
a memory struct (last seen position, time since seen, threat level).

## Avoiding thrashing
- Hysteresis: enter Chase when visible for 0.3 s, leave only after 2 s unseen.
- Distances: attack range enter 2.0 m, exit 2.5 m.
- Minimum time in state for animation-driven states.

## When FSMs stop scaling
Many states with near-identical transitions = use a hierarchical FSM (combat superstate with
substates) or move to behaviour trees/utility. F.E.A.R. replaced a complex FSM with 3 states
(Goto, Animate, UseSmartObject) plus GOAP planning (Jeff Orkin, GDC 2006).

## Verify
- Debug overlay shows state and suspicion per enemy; playtest stealth scenarios to confirm warnings
  are readable and states don't flicker.

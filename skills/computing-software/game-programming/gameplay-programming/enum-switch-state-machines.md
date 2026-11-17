---
id: computing-software.game-programming.gameplay-programming.enum-switch-state-machines
name: enum-switch-state-machines
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, state-machines, enum-state-machine, finite-state-machine, switch-statement, refactoring, game-programming]
level: intro
status: draft
description: "Write an enum-and-switch state machine correctly (single transition function, enter/exit hooks, timers) and recognise when it breaks and needs state objects or an HSM."
sources: ["https://gameprogrammingpatterns.com/state.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#match"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enum switch state machines and when they break

**Goal:** replace scattered booleans (`isJumping`, `isDucking`, `isDiving`) with one state variable,
using the simplest structure that works.

## Correct minimal form
```csharp
enum State { Idle, Run, Jump, Duck }
State state;
float stateTime;

void Update(float dt) {
    stateTime += dt;
    switch (state) {
        case State.Idle: if (input.Move != 0) ChangeState(State.Run);
                         if (input.JumpPressed) ChangeState(State.Jump); break;
        case State.Run:  Move(dt); if (input.Move == 0) ChangeState(State.Idle);
                         if (input.JumpPressed) ChangeState(State.Jump); break;
        case State.Jump: AirMove(dt); if (grounded && stateTime > 0.1f) ChangeState(State.Idle); break;
        case State.Duck: if (!input.Duck) ChangeState(State.Idle); break;
    }
}

void ChangeState(State next) {           // the ONLY place state is assigned
    if (next == state) return;
    switch (state) { case State.Duck: StandUp(); break; }          // exit
    state = next; stateTime = 0;
    switch (state) { case State.Jump: velocity.y = jumpSpeed; break;   // enter
                     case State.Duck: Crouch(); break; }
}
```
Rules: one assignment point, explicit enter/exit, per-state timer reset on entry, log transitions
(`Debug.Log($"{state} -> {next}")`) during development.

## When it breaks (refactor signals)
| Symptom | Move to |
|---|---|
| Each case grows past a screen; per-state fields pile up on the owner | State pattern objects with Enter/Update/Exit |
| Same transitions duplicated in many states (e.g. "hit -> Stagger" everywhere) | Hierarchical state machine (superstate handles it) |
| Two independent things change (movement + weapon) and states multiply (RunShooting, JumpShooting) | Concurrent state machines |
| Need "go back to previous" (pause, menus, interrupt then resume) | Pushdown automaton |
| Designers need to edit transitions | Data-driven transition tables or engine graphs (Animator, StateTree) |

Rough rule: up to ~5-7 states with simple transitions, the enum switch is the best choice: it is
readable top to bottom and trivially debuggable.

## Gotchas
- Assigning `state = X` directly anywhere else skips enter/exit and the timer reset.
- Transition in the middle of a case then continuing to run the old state's code the same frame:
  `return`/`break` right after `ChangeState`.
- Persist states by name, not int, if enums can be reordered.

## Verify
- [ ] grep shows a single `state =` assignment.
- [ ] Transition log for a play session has no unexpected edges.

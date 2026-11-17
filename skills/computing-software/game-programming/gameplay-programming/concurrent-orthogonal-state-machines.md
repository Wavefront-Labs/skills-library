---
id: computing-software.game-programming.gameplay-programming.concurrent-orthogonal-state-machines
name: concurrent-orthogonal-state-machines
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, concurrent-state-machines, orthogonal-regions, state-machine, game-programming]
level: practitioner
status: draft
description: "Split one exploding state machine into concurrent orthogonal machines (movement, weapon, posture) with explicit cross-machine guards."
sources: ["https://gameprogrammingpatterns.com/state.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Concurrent orthogonal state machines

**Goal:** stop the combinatorial blow-up where every combination (running+reloading, crouched+aiming)
becomes its own state.

## When to split
If the state count is roughly the product of two independent lists (N postures x M weapon states),
the axes are orthogonal. Nystrom's example: a heroine that can be standing/jumping/ducking *and*
armed/unarmed. Run one machine per axis.

```cpp
struct Character {
    MovementFSM movement;   // Idle, Run, Jump, Fall, Crouch
    WeaponFSM   weapon;     // Holstered, Ready, Firing, Reloading
    void handleInput(const Input& in) {
        movement.handleInput(*this, in);
        weapon.handleInput(*this, in);    // each machine sees the same input
    }
    void update(float dt) { movement.update(*this, dt); weapon.update(*this, dt); }
};
```

## Cross-machine rules
Orthogonal is rarely perfectly independent. Make interactions explicit and one-directional:
- **Guards that query the other machine:** `WeaponFSM::canFire()` returns false while
  `movement.is(Sprint)` or `movement.is(Climb)`. Query, never write, the other machine's state.
- **Events, not direct transitions:** movement entering `Climb` posts `HolsterRequest`; the weapon
  machine decides how to react on its own update.
- **Fixed update order:** decide which machine updates first and document it; otherwise a jump and
  a fire on the same frame resolve differently depending on order.
- **Input consumption:** if both machines map the same button (e.g. melee in either), give one
  priority and mark the input consumed.

## Statechart equivalent
UML/Harel statecharts call these *orthogonal regions* of one composite state. Libraries (QP, SCXML
runtimes, Unreal StateTree with parallel branches) implement it natively; hand-rolled, two machines
in a struct is enough.

## Pitfalls
- Hidden coupling: animation layers read both machines; keep the mapping in one place (an animation
  selector reading both states) rather than each machine poking the animator.
- Deadlock through mutual guards (A waits on B, B waits on A). Draw the guard graph; it must be acyclic.
- Save/load must serialise every region, not just the "main" one.

## Verify
- Count states before vs after; the split should turn N*M into N+M.
- Test every pair once with a table-driven test (posture x weapon) asserting allowed actions.

---
id: computing-software.game-programming.gameplay-programming.hierarchical-state-machines
name: hierarchical-state-machines
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-programming-patterns, hierarchical-state-machine, hfsm, statecharts, substates, state-pattern, game-programming]
level: practitioner
status: draft
description: "Build hierarchical state machines: superstates that handle shared input, unhandled events bubbling to parents, enter/exit order across levels and when to choose a behaviour tree."
sources: ["https://gameprogrammingpatterns.com/state.html#hierarchical-state-machines", "https://statecharts.dev/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hierarchical state machines

**Goal:** share behaviour between related states (standing, walking, ducking are all "on ground" and
all can jump) without copy-pasting the jump transition into each one.

## Idea
A state can have a **superstate**. Events the substate does not handle bubble up to the parent, like
method lookup in a class hierarchy (Nystrom). Harel statecharts formalise this.
```cpp
class OnGroundState : public HeroState {
public:
    HeroState* handleInput(Hero& h, const Input& in) override {
        if (in.pressed(BUTTON_B)) return new JumpingState();
        if (in.pressed(BUTTON_DOWN)) return new DuckingState();
        return nullptr;
    }
};
class DuckingState : public OnGroundState {
public:
    HeroState* handleInput(Hero& h, const Input& in) override {
        if (in.released(BUTTON_DOWN)) return new StandingState();
        return OnGroundState::handleInput(h, in);   // bubble up
    }
};
```
Inheritance works for one level. For deeper or data-driven trees, keep an explicit **stack of active
states** (root to leaf) and offer the event to the leaf first, then each parent.

## Enter/exit ordering
On a transition from leaf A to leaf B, find their lowest common ancestor (LCA):
1. exit from A up to (not including) the LCA, innermost first;
2. enter from below the LCA down to B, outermost first.
So `Ground.Walking -> Ground.Ducking` runs `Walking.exit, Ducking.enter` and leaves `Ground` active;
`Ground.Walking -> Air.Falling` runs `Walking.exit, Ground.exit, Air.enter, Falling.enter`.
Getting this wrong re-triggers parent side effects (footstep loop restarts on every ground substate change).

## Practical guidance
- Put shared transitions (stunned, dead, cutscene) at the root: any state can be interrupted once.
- Superstate data (time on ground, coyote timer) lives in the superstate, reset in its `enter`.
- History states: a superstate remembers its last active child to resume after an interrupt (e.g.
  return to the same combat substate after a hit-react).
- Keep depth at 2-3. Deep hierarchies make "who handled this input" hard to see; log the handling
  state for each event in debug builds.

## HFSM vs behaviour tree
HFSMs are explicit about states and transitions, good for player controllers and UI flow where you
must know the exact mode. Behaviour trees re-evaluate priorities every tick and suit AI choosing
among many actions; transitions are implicit. Unreal StateTree is a hybrid (hierarchical states
with selection conditions).

## Verify
- [ ] Each shared transition is written once (in the superstate).
- [ ] Unit test the enter/exit trace for sibling and cross-parent transitions against the LCA rule.
- [ ] Debug HUD prints the full active path (e.g. `Ground/Ducking`).

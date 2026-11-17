---
id: computing-software.game-programming.gameplay-programming.state-pattern-with-enter-exit
name: state-pattern-with-enter-exit
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-programming-patterns, state-pattern, finite-state-machine, fsm, enter-exit, player-states, game-programming]
level: practitioner
status: draft
description: "Replace boolean-flag soup with the State pattern: one object per state with enter/exit/update/handleInput, transitions returned by states, and static vs instantiated states."
sources: ["https://gameprogrammingpatterns.com/state.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State pattern with enter/exit

**Goal:** a character whose behaviour depends on mode (standing, jumping, ducking, diving) without
`isJumping && !isDucking` checks scattered through `update()` (Nystrom, GPP "State").

## Symptom that you need it
Flags that must never be true together (`isJumping`, `isDucking`, `isCharging`) and bugs like
"duck while jumping, then stand up mid-air". Each new feature adds another flag and another branch.

## Shape
```cpp
class HeroState {
public:
    virtual ~HeroState() = default;
    virtual void enter(Hero&) {}
    virtual void exit(Hero&) {}
    virtual HeroState* handleInput(Hero&, const Input&) { return nullptr; } // nullptr = stay
    virtual HeroState* update(Hero&, float dt) { return nullptr; }
};

class DuckingState : public HeroState {
    float chargeTime = 0;
public:
    void enter(Hero& h) override { h.setGraphics(IMAGE_DUCK); h.setHitbox(Hitbox::Low); }
    void exit(Hero& h) override  { h.setHitbox(Hitbox::Standing); }
    HeroState* handleInput(Hero&, const Input& in) override {
        return in.released(BUTTON_DOWN) ? new StandingState() : nullptr;
    }
    HeroState* update(Hero& h, float dt) override {
        if ((chargeTime += dt) > MAX_CHARGE) h.superBomb();
        return nullptr;
    }
};

void Hero::changeState(HeroState* next) {
    if (!next) return;
    state_->exit(*this);
    state_.reset(next);
    state_->enter(*this);   // enter sets graphics/hitbox: transitions no longer duplicate setup code
}
```

## Rules that keep it sane
- **Entry/exit own the side effects.** Animation, hitbox, sound and physics-mode changes go in
  `enter`/`exit`, never in the code that triggers the transition: every path into a state sets it up
  identically.
- **The state decides transitions** (return the next state) so the owner never switches on state type.
- **Defer the switch** to the end of the update when other systems may still be iterating; never
  delete the current state while its method is on the stack (return the new state, swap after).
- **Static vs instantiated states:** stateless states can be shared singletons (`static StandingState
  standing;`); states with fields (`chargeTime`) must be instantiated per owner.
- Keep a `const char* name()` per state for debug overlays and logs: "which state is it in" is the
  first question in every bug report.

## Engine equivalents
Unity: plain C# classes driven by a MonoBehaviour (Animator state machines are for animation, not
gameplay logic). Unreal: StateTree or a UObject state hierarchy. Godot: one child Node per state with
`enter()`/`exit()` and a parent machine node.

## Limits
A flat FSM struggles when states share behaviour (all on-ground states can jump) or when you must
return to the previous state: see `hierarchical-state-machines` and `pushdown-automaton-state-stack`.

## Verify
- [ ] Every transition path into a state produces the same animation/hitbox (enter owns setup).
- [ ] No gameplay code outside the machine checks the concrete state type.
- [ ] A debug overlay shows the current state name per character.

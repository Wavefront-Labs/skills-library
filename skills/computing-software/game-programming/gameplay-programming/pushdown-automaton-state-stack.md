---
id: computing-software.game-programming.gameplay-programming.pushdown-automaton-state-stack
name: pushdown-automaton-state-stack
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-programming-patterns, pushdown-automaton, state-stack, menu-stack, state-pattern, game-programming]
level: practitioner
status: draft
description: "Use a pushdown automaton (stack of states) to return to the previous state: firing then resuming, nested menus and modal popups, with pause/resume hooks and input routing."
sources: ["https://gameprogrammingpatterns.com/state.html#pushdown-automata", "https://gamedevelopment.tutsplus.com/tutorials/finite-state-machines-theory-and-implementation--gamedev-11867"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pushdown automaton (state stack)

**Goal:** enter a temporary state and come back to whatever was active before: the hero fires from
standing, running or jumping and must resume that state; a settings menu opened from the pause menu
or the title screen must return to its opener (Nystrom, GPP "Pushdown Automata").

## Operations
- `push(s)`: pause the top state, make `s` current.
- `pop()`: exit the top, resume the one below.
- `change(s)`: replace the top (a normal FSM transition).
```cpp
class StateStack {
    std::vector<std::unique_ptr<State>> stack_;
    enum class Op { Push, Pop, Change }; struct Pending { Op op; std::unique_ptr<State> s; };
    std::vector<Pending> pending_;          // applied after update: never mutate while iterating
public:
    void push(std::unique_ptr<State> s)   { pending_.push_back({Op::Push, std::move(s)}); }
    void pop()                            { pending_.push_back({Op::Pop, nullptr}); }
    void change(std::unique_ptr<State> s) { pending_.push_back({Op::Change, std::move(s)}); }
    void update(float dt) {
        if (!stack_.empty()) stack_.back()->update(*this, dt);
        for (auto& p : pending_) {
            if (p.op != Op::Push && !stack_.empty()) { stack_.back()->exit(); stack_.pop_back(); }
            else if (p.op == Op::Push && !stack_.empty()) stack_.back()->pause();
            if (p.s) { stack_.push_back(std::move(p.s)); stack_.back()->enter(); }
            else if (!stack_.empty()) stack_.back()->resume();
        }
        pending_.clear();
    }
};
```

## Hooks: enter/exit vs pause/resume
Separate them. `pause` on the gameplay state when a menu is pushed stops music ducking twice and
keeps the level loaded; `exit` would tear it down. `resume` restores input focus and cursor mode.

## Menu and popup stacks
- Only the **top** state receives input; lower states may still **draw** (pause menu over the frozen
  game). Give states flags: `blocksUpdateBelow`, `blocksDrawBelow`, `blocksInputBelow`.
- Back/Escape = `pop()`. Never let the root state pop (title or gameplay).
- Confirm dialogs push on top of whatever asked; the result comes back via a callback or the
  `resume(result)` hook, not a global.

## Pitfalls
- Immediate push/pop inside `update` invalidates the iterator or deletes the running state: queue ops.
- Pushing the same modal twice (double-click) stacks duplicates; guard by type or debounce.
- Save/load: decide whether the stack serialises (usually only the root gameplay state does).

## Verify
- [ ] Fire from standing, running and jumping returns to the same state each time.
- [ ] Settings opened from pause and from title both return to their opener with Back.
- [ ] Spamming Back from a 3-deep menu never empties the stack.

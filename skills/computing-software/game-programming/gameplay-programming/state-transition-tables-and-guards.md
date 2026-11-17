---
id: computing-software.game-programming.gameplay-programming.state-transition-tables-and-guards
name: state-transition-tables-and-guards
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, finite-state-machine, transition-table, transition-guards, state-chart, game-programming]
level: practitioner
status: draft
description: "Drive gameplay FSMs from transition tables with guards and actions instead of scattered if-chains: table layout, any-state transitions, priorities, and validating the table."
sources: ["https://gameprogrammingpatterns.com/state.html", "https://statecharts.dev/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transition tables and guards

**Goal:** state machines whose transitions are data you can read, test and validate, not logic spread
across every state's update.

## Table shape
Each row: `from`, `event or condition`, `guard`, `to`, `action`, `priority`.
```csharp
record Transition(State From, Trigger On, Func<bool> Guard, State To, Action Effect = null, int Priority = 0);
readonly List<Transition> table = new() {
    new(State.Idle,   Trigger.MoveInput, () => grounded,          State.Run),
    new(State.Run,    Trigger.JumpPressed, () => grounded,        State.Jump, Effect: DoJump),
    new(State.Jump,   Trigger.Tick,   () => velocity.y < 0,       State.Fall),
    new(State.Fall,   Trigger.Tick,   () => grounded,             State.Land, Effect: PlayLandFx),
    new(State.Any,    Trigger.Damaged, () => !invulnerable,       State.HitStun, Priority: 10),
};
public void Fire(Trigger t) {
    foreach (var tr in table.Where(x => (x.From == current || x.From == State.Any) && x.On == t)
                            .OrderByDescending(x => x.Priority)) {
        if (tr.Guard()) { Exit(current); tr.Effect?.Invoke(); current = tr.To; Enter(current); return; }
    }
}
```
(Precompute per-state lists at startup instead of LINQ per call in hot paths.)

## Guards
- Pure boolean checks on context; no side effects (so tables can be evaluated speculatively/tested).
- Common: grounded, has stamina, cooldown ready, not stunned, animation in cancel window.

## Event vs condition transitions
- Event-driven (`JumpPressed`, `Damaged`): fired by systems.
- Polled (`Tick`): evaluated each update for conditions like "velocity.y < 0".
Mixing both is normal; keep the polled set small for cost and clarity.

## Any-state and priority
Global transitions (damage, death, cutscene) come from `Any`; priority resolves conflicts when multiple
guards pass (death > hit-stun > movement). Explicitly exclude states (death shouldn't re-enter from dead).

## Validation (do this; it's the point of tables)
- Unreachable states (no incoming transitions).
- Dead ends (no outgoing, except terminal states).
- Ambiguity: two rows same from/trigger/priority with overlapping guards.
- Export to Graphviz/Mermaid for design review.

## Gotchas
- Effects that fire triggers recursively: queue triggers raised during a transition and process after.
- Tables in data files (designer-editable) need named guards/actions registered from code.

## Verify
- [ ] Unit tests per row: given state + trigger + guard values, expect target state.
- [ ] Validator runs at startup in dev builds and logs problems.

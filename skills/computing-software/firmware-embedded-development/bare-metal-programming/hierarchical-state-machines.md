---
id: computing-software.firmware-embedded-development.bare-metal-programming.hierarchical-state-machines
name: hierarchical-state-machines
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [hierarchical-state-machine, hsm, uml-statechart, state-machine, qp-framework, qm, entry-exit-actions, run-to-completion, event-driven, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Design and code hierarchical state machines (UML statecharts) in C: superstates, entry/exit ordering, LCA transitions, internal vs self transitions, and the QP/C handler style."
sources:
  - https://www.state-machine.com/doc/AN_Crash_Course_in_UML_State_Machines.pdf
  - https://github.com/QuantumLeaps/qpc/blob/master/include/qp.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hierarchical state machines

**Goal:** replace flag-and-if spaghetti in device control code with a statechart whose
behaviour is inspectable and testable on the host, and does not explode in states.

## Why hierarchy
A flat FSM for a device with `off/idle/measuring/error` plus "any state: on `POWER_FAIL` go
to `safe`" duplicates the power-fail transition in every state. A superstate `on` that
contains `idle/measuring` handles `POWER_FAIL` once; substates inherit it. The Quantum Leaps
"Crash Course in UML State Machines" calls this behavioral inheritance: substates define only
the differences from the superstate, and unhandled events flow back up to the higher level.

## Semantics to get right
- **Run-to-completion**: all actions triggered by an event must complete before the next
  event is dispatched, so the machine starts each event in a stable state configuration.
  Never dispatch a new event from inside a handler.
- **Transition order** (UML): evaluate the guard; exit states from the active state up to, but
  not including, the **least common ancestor (LCA)** of source and target, innermost first; run
  the transition action; enter states from inside the LCA down to the target; if the target is
  composite, drill into it with initial transitions until a leaf.
  The QP "Practical UML Statecharts" implementation keeps the exit-then-enter order but runs the
  transition action in the context of the source state, before the source is exited.
- **Self-transition** runs the exit and entry actions of the state; an **internal
  transition** never runs entry or exit actions, even when it is inherited from a higher level.
- Entry and exit actions give guaranteed initialisation and cleanup without repeating that code on
  every transition into or out of the state.

## State-handler style (QP/C pattern)
```c
static QState Blinky_on(void * const me, QEvt const * const e) {
    switch (e->sig) {
    case Q_ENTRY_SIG:  led_on(); QTimeEvt_armX(&((Blinky *)me)->te, TICKS_1S, 0U); return Q_HANDLED();
    case Q_EXIT_SIG:   QTimeEvt_disarm(&((Blinky *)me)->te); return Q_HANDLED();
    case TIMEOUT_SIG:  return Q_TRAN(&Blinky_off);
    case POWER_FAIL_SIG: return Q_TRAN(&Blinky_safe);
    }
    return Q_SUPER(&Blinky_operational);   /* parent handles everything else */
}
```
The `qp.h` header defines `Q_ENTRY_SIG`, `Q_EXIT_SIG`, `Q_TRAN`, `Q_SUPER`, `Q_HANDLED`,
`QTimeEvt_armX(me, nTicks, interval)` and `QTimeEvt_disarm`. Each state is a function; returning
`Q_SUPER(parent)` names the parent, and the framework works out the LCA path. Signal names
(`TIMEOUT_SIG`, `POWER_FAIL_SIG`) and the states are application-defined. A hand-rolled design
needs the same parent lookup.

## Design workflow
1. List events (signals) and the extended state variables.
2. Draw the statechart; find transitions common to several states and lift them into superstates.
3. Keep states few and meaningful; push counters and values into extended state with guards
   rather than one state per value.
4. Unit-test on the host: feed event sequences, assert on a trace of entry, exit and actions.

## Gotchas
- Blocking calls inside actions break run-to-completion timing; use events and timers.
- Check each event's handling at every level: an event a substate should inherit but handles itself
  hides the superstate transition.

## Verify
- [ ] Host test prints the exact exit/entry sequence for every transition crossing levels.
- [ ] No state handles an event it should have inherited (duplicated transitions removed).

## Checked
Method: docs-checked 2026-11-09 against the Quantum Leaps "A Crash Course in UML State Machines" PDF (downloaded, converted with pdftotext; read behavioral inheritance, entry/exit actions, internal vs self-transitions, LCA transition sequence and the QP implementation note, run-to-completion definition) and the QP/C `qp.h` header on GitHub (signal and macro names, `QTimeEvt_armX` and `QTimeEvt_disarm` signatures, state-handler typedef).
Removed as unconfirmed: history pseudostate advice, tool names for drawing statecharts, the remark on generated transition tables, and the `Blinky * const me` handler signature (the header types `me` as a void pointer). The QP/C landing page and UML 2.5.1 specification were not used.

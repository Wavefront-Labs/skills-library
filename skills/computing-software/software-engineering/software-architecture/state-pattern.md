---
id: computing-software.software-engineering.software-architecture.state-pattern
name: state-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, behavioral-patterns, state-pattern, gof, state-machine, finite-state-machine, transitions]
level: practitioner
status: verified
description: "Model object behaviour that depends on its state with the State pattern or an explicit state machine; transition tables, illegal transitions, persistence and testing."
sources:
  - https://refactoring.guru/design-patterns/state
  - https://gameprogrammingpatterns.com/state.html
  - https://stately.ai/docs/state-machines-and-statecharts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State pattern and explicit state machines

**Intent (GoF):** allow an object to alter its behaviour when its internal state changes; the object will appear to change its class.

## Smell that calls for it
Every method starts with `if self.status == "draft": ... elif self.status == "submitted": ...` and the same status checks repeat across methods. Illegal transitions are possible because any code can assign `status`.

## Option 1: State objects (GoF)
```python
class Draft:
    def submit(self, doc): doc.state = Submitted()
    def approve(self, doc): raise InvalidTransition("draft -> approved")

class Submitted:
    def submit(self, doc): raise InvalidTransition("already submitted")
    def approve(self, doc): doc.state = Approved(); doc.notify_owner()

class Approved:                                   # terminal: every event is illegal
    def submit(self, doc): raise InvalidTransition("approved is final")
    approve = submit
class Document:
    def __init__(self): self.state = Draft()
    def submit(self): self.state.submit(self)
    def approve(self): self.state.approve(self)
```
Good when each state has substantial distinct behaviour.

## Option 2: Transition table (often simpler)
```python
TRANSITIONS = {
    ("draft", "submit"): "submitted",
    ("submitted", "approve"): "approved",
    ("submitted", "reject"): "draft",
}
def fire(doc, event):
    try: doc.status = TRANSITIONS[(doc.status, event)]
    except KeyError: raise InvalidTransition(doc.status, event)
```
The table is data: render it as a diagram, test it exhaustively, review it in one place. Libraries: XState (JS statecharts), Spring Statemachine, `transitions` (Python), Stateless (.NET).

## Practical rules
- Make the state field private; the only way to change it is through events.
- Persist the state name (string/enum), not the state object; rehydrate on load.
- Put side effects (emails, charges) on transitions, and run them after the state change commits (outbox) so a retry does not double-fire.
- Concurrent events on the same entity: use optimistic locking (version column) so two transitions cannot both succeed from the same source state.
- Hierarchical/parallel states (statecharts) when the flat machine explodes combinatorially.

## Verify
- [ ] Test every (state, event) pair: allowed pairs reach the expected state, others raise.
- [ ] Generate the diagram from the table and check it matches the product spec.

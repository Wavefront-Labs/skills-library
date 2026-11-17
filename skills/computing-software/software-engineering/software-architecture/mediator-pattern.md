---
id: computing-software.software-engineering.software-architecture.mediator-pattern
name: mediator-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, behavioral-patterns, mediator-pattern, gof, coupling, event-bus, mediatr]
level: practitioner
status: verified
description: "Use the Mediator pattern to replace many-to-many object coupling with a coordinating object; UI dialogs, in-process request dispatch (MediatR) and avoiding a god mediator."
sources:
  - https://refactoring.guru/design-patterns/mediator
  - https://github.com/jbogard/MediatR/wiki
  - https://en.wikipedia.org/wiki/Mediator_pattern
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mediator pattern

**Intent (GoF):** define an object that encapsulates how a set of objects interact, promoting loose coupling by keeping objects from referring to each other explicitly.

## Smell
N components that all reference each other (a form where the country dropdown updates the state list, which enables the postcode field, which toggles the submit button...). Each new component touches every other one: O(n^2) links.

## Shape (UI coordination)
```python
class CheckoutDialog:          # the mediator
    def __init__(self):
        self.country = Dropdown(on_change=self.changed)
        self.state   = Dropdown(on_change=self.changed)
        self.submit  = Button()
    def changed(self, sender):
        if sender is self.country:
            self.state.set_options(states_for(self.country.value))
            self.state.value = None            # a stale state must not survive a country change
        self.submit.enabled = bool(self.country.value and self.state.value)
```
Components only know the mediator callback; interaction rules live in one place.

## In-process request mediator (MediatR style)
Controllers send `CreateOrder` to `mediator.Send(cmd)`; the mediator finds the single handler and runs pipeline behaviours (validation, logging, transactions) around it. Benefits: thin controllers, cross-cutting behaviours in one pipeline. Costs: indirection - "go to definition" no longer finds the handler, so keep handler names tied to request names (`CreateOrderHandler`). Do not adopt it in a small codebase just for the pattern.

## Mediator vs Observer vs Facade
- Observer: one-way broadcast; subject has no coordination logic.
- Mediator: two-way coordination with rules.
- Facade: simplifies a subsystem for outside callers; subsystem classes do not know the facade.

## Pitfalls
- **God mediator:** all business logic migrates into one class. Split by workflow (one mediator per dialog or use case).
- Hidden control flow; log which handler ran for each request.

## Verify
- [ ] Components are unit-testable with a fake mediator; no component imports another.
- [ ] Mediator rules have table-driven tests (input change -> expected component states).

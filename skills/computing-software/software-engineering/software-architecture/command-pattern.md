---
id: computing-software.software-engineering.software-architecture.command-pattern
name: command-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, behavioral-patterns, command-pattern, gof, undo-redo, job-queue, request-objects]
level: practitioner
status: verified
description: "Use the Command pattern to turn requests into objects for undo/redo, queuing, retries and audit logs; covers command vs handler split and serialisable commands."
sources:
  - https://refactoring.guru/design-patterns/command
  - https://en.wikipedia.org/wiki/Command_pattern
  - https://gameprogrammingpatterns.com/command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Command pattern

**Intent (GoF):** encapsulate a request as an object, letting you parameterise clients with requests, queue or log them, and support undoable operations.

## Use it when
- Undo/redo in editors and design tools.
- Work must be queued, scheduled, retried, or executed on another machine (job queues).
- You need an audit log of intents, or macro recording (a list of commands replayed).
- UI actions (menu item, shortcut, toolbar button) should share one action object with `canExecute` state.

## Shape (undoable)
```python
class Command(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...

@dataclass
class MoveShape:
    shape: Shape
    dx: int
    dy: int
    def execute(self): self.shape.move(self.dx, self.dy)
    def undo(self):    self.shape.move(-self.dx, -self.dy)

class History:
    def __init__(self): self.done, self.undone = [], []
    def run(self, cmd):
        cmd.execute(); self.done.append(cmd); self.undone.clear()   # new action kills redo stack
    def undo(self):
        if self.done: c = self.done.pop(); c.undo(); self.undone.append(c)
    def redo(self):
        if self.undone: c = self.undone.pop(); c.execute(); self.done.append(c)
```

## Undo strategies
- **Inverse operation** (above): cheap, but every command must be exactly reversible, including side effects.
- **Memento:** snapshot state before execute and restore on undo; simpler, costs memory. Use for operations with no clean inverse.
- Merge consecutive small commands (each keystroke) into one undo step with a `merge_with(other)` hook.

## Queued and distributed commands
Split the data (`ChargeCard{order_id, amount, idempotency_key}`) from the handler (`ChargeCardHandler`). The data is serialisable for queues and logs; the handler holds dependencies. This is the CQRS command / message-handler style used by MediatR, Axon, Symfony Messenger. Give each command an id so retries are idempotent.

## Pitfalls
- Commands holding live references to objects that are later deleted: undo then resurrects garbage; store ids and re-resolve.
- A command class for every trivial call adds ceremony; a closure works when undo/queueing is not needed.

## Verify
- [ ] Property test: random sequences of run/undo/redo return the document to the expected state.
- [ ] Queued commands survive a serialise/deserialise round trip.

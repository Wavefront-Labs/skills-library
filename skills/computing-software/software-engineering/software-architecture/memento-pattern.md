---
id: computing-software.software-engineering.software-architecture.memento-pattern
name: memento-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, behavioral-patterns, memento-pattern, gof, undo, snapshots, state-restoration]
level: practitioner
status: verified
description: "Use the Memento pattern to snapshot and restore object state without breaking encapsulation: undo stacks, checkpoints, memory limits and structural sharing."
sources:
  - https://refactoring.guru/design-patterns/memento
  - https://en.wikipedia.org/wiki/Memento_pattern
  - https://immerjs.github.io/immer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memento pattern

**Intent (GoF):** without violating encapsulation, capture and externalise an object's internal state so the object can be restored to it later.

## Roles
- **Originator:** the object whose state is saved; creates and restores mementos.
- **Memento:** opaque snapshot; only the originator can read it.
- **Caretaker:** holds mementos (undo stack, checkpoint list) without inspecting them.

## Shape
```python
@dataclass(frozen=True)
class _EditorMemento:          # leading underscore: opaque to callers
    text: str
    cursor: int

class Editor:
    def __init__(self): self.text, self.cursor = "", 0
    def save(self) -> _EditorMemento: return _EditorMemento(self.text, self.cursor)
    def restore(self, m: _EditorMemento): self.text, self.cursor = m.text, m.cursor

history: list[_EditorMemento] = []
history.append(editor.save()); editor.type("hello")
editor.restore(history.pop())     # undo (add `from dataclasses import dataclass` and an `Editor.type` method to run it; with those it restores text '' and cursor 0)
```
In Java/C# make the memento a nested class with private fields so only the originator can read it.

## Memory management
- Full snapshots of big state are expensive. Use **structural sharing** with immutable data (Immer, Immutable.js, persistent collections, Clojure): each snapshot shares unchanged subtrees, so copies are O(changed).
- Cap the history (ring buffer, last N steps) or coalesce snapshots over time.
- Snapshot only state the user can undo; derived caches are rebuilt on restore.

## Memento vs Command undo
Command undo applies inverse operations (small memory, needs exact inverses). Memento restores snapshots (simple, robust to complex operations, more memory). Many editors combine them: commands that store a memento of what they touched.

## Pitfalls
- Shallow copies: a memento that holds references to mutable lists changes when the originator changes. Deep-copy or use immutable values.
- Restoring state that references external resources (open files, sockets, ids issued by a server) - snapshot identifiers, not handles.
- Serialised mementos (save games, drafts) need a schema version for future migrations.

## Verify
- [ ] Mutate after save, restore, and assert equality with the saved state (catches shallow copies).
- [ ] Memory profile of a long session stays bounded with the history cap.

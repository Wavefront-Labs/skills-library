---
id: computing-software.software-engineering.ada.task-types-entries
name: task-types-entries
category: computing-software
field: software-engineering
product: ada
tags: [ada, task-types-entries, ada-tasking]
level: practitioner
status: draft
description: "Declare Ada tasks and task types, entries, accept statements, rendezvous parameters and task termination."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Task types, entries and rendezvous
```ada
task type Worker is
   entry Start (N : Integer);
end Worker;
task body Worker is
begin
   accept Start (N : Integer) do ... end Start;
end Worker;
W : Worker;
```
- A task activates when its declarative part finishes elaborating; the enclosing scope waits for its dependents.
- `Task'Terminated`, `'Callable`; `Ada.Task_Identification`.
- Plain `task Name;` creates a single task object.
## Gotchas
- Main program does not exit until all dependent tasks terminate.
- Unhandled exceptions in tasks end only that task, silently.
## Self-check
Start 3 workers and confirm the program exits only after all finish.

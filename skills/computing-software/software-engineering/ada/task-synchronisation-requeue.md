---
id: computing-software.software-engineering.ada.task-synchronisation-requeue
name: task-synchronisation-requeue
category: computing-software
field: software-engineering
product: ada
tags: [ada, task-synchronisation-requeue]
level: advanced
status: draft
description: "Ada entry families, entry queues, 'Count, guarded accept and requeue for task coordination."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/advanced-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Entry families, queues and requeue
```ada
task Server is entry Request (1 .. 4) (Data : Integer); end Server;
select accept Request (I) (Data : Integer) do ... end;
```
- FIFO queue per entry by default.
- `requeue Other_Entry with abort;` moves the caller to another entry without releasing it.
- `Entry'Count` gives current queue length (may be stale).
## Gotchas
- Rendezvous couples caller and callee in time; use protected objects for data sharing.
## Self-check
Queue two callers on one entry and observe FIFO order.

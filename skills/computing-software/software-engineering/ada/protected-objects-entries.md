---
id: computing-software.software-engineering.ada.protected-objects-entries
name: protected-objects-entries
category: computing-software
field: software-engineering
product: ada
tags: [ada, protected-objects-entries, ada-protected]
level: practitioner
status: draft
description: "Ada protected types: read-only functions, exclusive procedures, entries with barriers; mutual exclusion without locks."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Protected objects, functions, procedures and entries
```ada
protected type Counter is
   function Value return Natural;
   procedure Inc;
   entry Wait_Positive;
private
   N : Natural := 0;
end Counter;
protected body Counter is
   function Value return Natural is (N);
   procedure Inc is begin N := N + 1; end;
   entry Wait_Positive when N > 0 is begin null; end;
end Counter;
```
- Functions run concurrently (read lock); procedures and entries are exclusive.
- Barriers are re-evaluated when the protected state changes.
## Gotchas
- Never call a potentially blocking operation (delay, entry call, I/O) inside a protected action.
## Self-check
Increment from 8 tasks and confirm the final count.

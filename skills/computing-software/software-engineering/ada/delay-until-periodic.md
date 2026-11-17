---
id: computing-software.software-engineering.ada.delay-until-periodic
name: delay-until-periodic
category: computing-software
field: software-engineering
product: ada
tags: [ada, delay-until-periodic, ada-real-time]
level: practitioner
status: draft
description: "Periodic Ada tasks with delay until and Ada.Real_Time.Clock to avoid cumulative drift."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/advanced-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# delay and delay until: periodic tasks
```ada
with Ada.Real_Time; use Ada.Real_Time;
Next : Time := Clock;
Period : constant Time_Span := Milliseconds (100);
loop
   Do_Work;
   Next := Next + Period;
   delay until Next;
end loop;
```
- `delay D;` sleeps relative to now (drifts); `delay until T;` is absolute.
- `Ada.Real_Time` is monotonic; `Ada.Calendar` follows wall-clock changes.
## Gotchas
- Check overrun: if Clock > Next, you missed the deadline.
## Self-check
Log Clock for 10 iterations and confirm average period equals Period.

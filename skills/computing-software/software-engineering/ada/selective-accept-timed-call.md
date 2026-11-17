---
id: computing-software.software-engineering.ada.selective-accept-timed-call
name: selective-accept-timed-call
category: computing-software
field: software-engineering
product: ada
tags: [ada, selective-accept-timed-call, ada-select-abort]
level: advanced
status: draft
description: "Ada select statement forms: selective accept with guards and terminate, timed and conditional entry calls."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/advanced-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Selective accept and timed entry calls
```ada
select
   when Ready => accept Go;
or accept Stop do Quit := True; end;
or delay 1.0;
or terminate;
end select;
select Server.Request (1); or delay 0.5; Put_Line ("timeout"); end select; -- timed
select Server.Request (1); else Put_Line ("busy"); end select;            -- conditional
```
- `terminate` only when no more callers can arrive.
- Only one of delay / terminate / else per accept select.
## Gotchas
- A timed call times out on the wait to be accepted, not on the rendezvous duration.
## Self-check
Time out a call to a task that never accepts.

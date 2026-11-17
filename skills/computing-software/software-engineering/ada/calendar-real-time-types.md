---
id: computing-software.software-engineering.ada.calendar-real-time-types
name: calendar-real-time-types
category: computing-software
field: software-engineering
product: ada
tags: [ada, calendar-real-time-types]
level: intro
status: draft
description: "Time_Span, Time, Duration, Ada.Calendar Year/Month/Day/Seconds and Ada.Calendar.Formatting Image."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ada.Calendar and Ada.Real_Time types
```ada
with Ada.Calendar; with Ada.Calendar.Formatting;
Now : Ada.Calendar.Time := Ada.Calendar.Clock;
Put_Line (Ada.Calendar.Formatting.Image (Now));
D : Duration := 1.5;   -- fixed point seconds
```
- `Ada.Real_Time`: `Milliseconds`, `Seconds`, `To_Duration`, `Time_Span_Zero`.
- `Duration` is a fixed-point type in seconds; `delay` takes it.
## Gotchas
- Calendar time can jump (NTP, DST via UTC offset functions).
## Self-check
Convert a Time_Span to Duration and delay by it.

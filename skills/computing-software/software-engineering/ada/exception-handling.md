---
id: computing-software.software-engineering.ada.exception-handling
name: exception-handling
category: computing-software
field: software-engineering
product: ada
tags: [ada, exception-handling, ada-exceptions]
level: practitioner
status: docs-checked
description: "Ada exception declaration, raise, handlers, others, re-raise, Constraint_Error/Program_Error/Storage_Error/Tasking_Error."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raising and handling exceptions
```ada
My_Error : exception;
begin
   raise My_Error with "bad input";
exception
   when Constraint_Error => Put_Line ("range");
   when E : others => Put_Line (Ada.Exceptions.Exception_Message (E)); raise;
end;
```
- Predefined: `Constraint_Error` (the one you see most), `Program_Error` (elaboration-order issues, some erroneous execution), `Storage_Error` (memory problems), `Tasking_Error` (errors such as failure during task activation).
- `Exception_Message` from `Ada.Exceptions` returns the text given after `with`.
## Gotchas
- A bare `raise;` inside a handler re-raises the current exception.
## Self-check
Raise from a nested call and catch two frames up.

## Checked
2026-11-03. Confirmed in Introduction to Ada, Exceptions: `raise X with "message"`, `Exception_Message`, bare `raise;`, `when others`, the four predefined exceptions and what raises them. Removed the frame/locals claim and the unhandled-exception behaviour for main and tasks (not on the pages read).
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.ada.exception-occurrence-info
name: exception-occurrence-info
category: computing-software
field: software-engineering
product: ada
tags: [ada, exception-occurrence-info]
level: advanced
status: docs-checked
description: "Use Exception_Message from Ada.Exceptions in handlers, and GNAT's gnatbind -Es/-Ea tracebacks (GNAT.Traceback)."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exception occurrences and messages
```ada
with Ada.Exceptions;
exception when E : others =>
   Put_Line (Ada.Exceptions.Exception_Message (E));
```
- `Exception_Message` returns the message associated with the exception as a string.
- gnatbind `-Es` stores symbolic tracebacks in exception occurrences, `-Ea` (same as `-E`) stores hexadecimal addresses, when the target supports it; see `GNAT.Traceback` and `GNAT.Traceback.Symbolic`.
- On x86 do not use `-fomit-frame-pointer` when you want tracebacks.
## Gotchas
- Exception_Message is the text after `with`.
## Self-check
Print Exception_Message from a deliberate Constraint_Error.

## Checked
2026-11-03. Confirmed in Introduction to Ada, Exceptions (`Exception_Message`) and the GNAT User's Guide gnatbind switches (`-E`, `-Ea`, `-Es`, GNAT.Traceback, frame pointer note). Removed `Exception_Information`, `Exception_Name`, `Save_Occurrence`, `Exception_Identity`, `Raise_Exception` and the `--export-dynamic` linker flag (not on the pages read).
Method: documentation only; no commands were run.

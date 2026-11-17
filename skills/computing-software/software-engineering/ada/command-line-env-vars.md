---
id: computing-software.software-engineering.ada.command-line-env-vars
name: command-line-env-vars
category: computing-software
field: software-engineering
product: ada
tags: [ada, command-line-env-vars, ada-environment]
level: intro
status: draft
description: "Ada.Command_Line Argument_Count/Argument/Set_Exit_Status and Ada.Environment_Variables."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Command line and environment variables
```ada
with Ada.Command_Line; with Ada.Environment_Variables;
for I in 1 .. Ada.Command_Line.Argument_Count loop
   Put_Line (Ada.Command_Line.Argument (I));
end loop;
Ada.Command_Line.Set_Exit_Status (Ada.Command_Line.Failure);
if Ada.Environment_Variables.Exists ("HOME") then ... end if;
```
- `Command_Name` gives program path.
- Use `GNAT.Command_Line` for option parsing.
## Gotchas
- `Argument (0)` raises `Constraint_Error`.
## Self-check
Print all args and exit with failure; check shell status.

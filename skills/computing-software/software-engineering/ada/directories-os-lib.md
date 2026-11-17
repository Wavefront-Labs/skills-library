---
id: computing-software.software-engineering.ada.directories-os-lib
name: directories-os-lib
category: computing-software
field: software-engineering
product: ada
tags: [ada, directories-os-lib]
level: practitioner
status: draft
description: "Files and processes in Ada: Ada.Directories Exists/Create_Path/Search, GNAT.OS_Lib Spawn and Getenv."
sources:
  - https://www.ada-auth.org/standards/
  - https://docs.adacore.com/gnat_rm-docs/html/gnat_rm/gnat_rm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ada.Directories and GNAT.OS_Lib
```ada
with Ada.Directories;
if Ada.Directories.Exists ("out") then Ada.Directories.Delete_Tree ("out"); end if;
Ada.Directories.Create_Path ("out/a");
Search (".", "*.adb", Process => Handle'Access);
with GNAT.OS_Lib;
Rc := GNAT.OS_Lib.Spawn ("/bin/ls", Args);  -- Args : Argument_List
```
- `Ada.Directories.Simple_Name`, `Containing_Directory`, `Full_Name`.
- Spawn takes a program path and argument list, not a shell string.
## Gotchas
- `Delete_Tree` is irreversible.
## Self-check
List *.ads files in a temp dir you create.

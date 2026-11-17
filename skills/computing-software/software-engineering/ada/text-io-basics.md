---
id: computing-software.software-engineering.ada.text-io-basics
name: text-io-basics
category: computing-software
field: software-engineering
product: ada
tags: [ada, text-io-basics, ada-text-io]
level: intro
status: draft
description: "Ada.Text_IO Put_Line, Get_Line, Ada.Integer_Text_IO, Text_IO files, and File_Type Open/Create/Close."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Text_IO basics
```ada
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Integer_Text_IO;
F : File_Type;
Open (F, In_File, "data.txt");
while not End_Of_File (F) loop Put_Line (Get_Line (F)); end loop;
Close (F);
Ada.Integer_Text_IO.Get (N);   Put (N, Width => 4);
```
- Handle `Name_Error`, `Data_Error`, `End_Error`, `Use_Error` explicitly.
- `Ada.Text_IO.Enumeration_IO` and `Float_IO` are generics: instantiate for your type.
## Gotchas
- `Get` leaves the line terminator; follow with `Skip_Line` before `Get_Line`.
## Self-check
Read a missing file and catch Name_Error.

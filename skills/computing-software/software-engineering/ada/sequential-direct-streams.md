---
id: computing-software.software-engineering.ada.sequential-direct-streams
name: sequential-direct-streams
category: computing-software
field: software-engineering
product: ada
tags: [ada, sequential-direct-streams]
level: practitioner
status: draft
description: "Binary IO in Ada: Sequential_IO, Direct_IO, Ada.Streams.Stream_IO and the 'Read/'Write/'Input/'Output attributes."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/advanced-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sequential, Direct and Stream IO
```ada
with Ada.Streams.Stream_IO; use Ada.Streams.Stream_IO;
F : File_Type;
Create (F, Out_File, "x.bin");
Integer'Write (Stream (F), 42);
Point'Output (Stream (F), P);   -- writes bounds/discriminants too
```
- `'Write`/`'Read` omit bounds/tags; `'Output`/`'Input` include them.
- Override with `for T'Write use My_Write;` or aspect `Write => My_Write`.
## Gotchas
- Stream format of Float and Integer is target-specific unless the type sizes match.
## Self-check
Write a record then read it back and compare.

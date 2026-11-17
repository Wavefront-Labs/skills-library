---
id: computing-software.software-engineering.ada.gpr-project-files
name: gpr-project-files
category: computing-software
field: software-engineering
product: ada
tags: [ada, gpr-project-files, gnat-gpr]
level: practitioner
status: docs-checked
description: "Write .gpr files: Source_Dirs, Object_Dir, Main, Exec_Dir, Compiler package, scenario variables, gprbuild -P."
sources:
  - https://docs.adacore.com/gprbuild-docs/html/gprbuild_ug.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project files: sources, objects, builder
```
project App is
   for Source_Dirs use ("src");
   for Object_Dir use "obj";
   for Main use ("main.adb");
   type Mode_Type is ("debug", "release");
   Mode : Mode_Type := external ("MODE", "debug");
   package Compiler is
      case Mode is
         when "debug"   => for Default_Switches ("ada") use ("-g", "-gnata");
         when "release" => for Default_Switches ("ada") use ("-O2");
      end case;
   end Compiler;
end App;
```
- Build: `gprbuild -P app.gpr -XMODE=release`.
- `-v` makes gprbuild print the full compile and link commands, so you can compare switches between modes.
## Gotchas
- If `Object_Dir` is not set it defaults to the directory containing the project file; the directory must already exist (gprbuild `-p` creates missing ones).
- Without `Exec_Dir` the executable goes in the object directory.
## Self-check
Build in both modes and verify different switches via `gprbuild -v`.

## Checked
2026-11-03. Confirmed in the GPRbuild User's Guide (GNAT Project Manager chapter): `Object_Dir` default and `-p`, `Exec_Dir` default, `Default_Switches` indexed by language, `-P` and `-X`, scenario variables with `external` and `case`, `-v` verbose output. Removed `gprclean` (not on the pages read) and the claim that objects go to the source dir.
Method: documentation only; no commands were run.

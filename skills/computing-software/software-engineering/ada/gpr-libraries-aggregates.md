---
id: computing-software.software-engineering.ada.gpr-libraries-aggregates
name: gpr-libraries-aggregates
category: computing-software
field: software-engineering
product: ada
tags: [ada, gpr-libraries-aggregates]
level: advanced
status: docs-checked
description: "gprbuild library projects (Library_Name, Library_Dir, Library_Kind), project extension 'extends', and aggregate projects."
sources:
  - https://docs.adacore.com/gprbuild-docs/html/gprbuild_ug.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Library projects, extending, aggregates
```
library project Lib is
   for Library_Name use "lib"; for Library_Dir use "lib";
   for Library_Kind use "static";    -- or static-pic / dynamic / relocatable
end Lib;
with "lib.gpr"; project App is ... end App;
aggregate project All_Prj is for Project_Files use ("a.gpr", "b.gpr"); end All_Prj;
```
- `project X extends "base.gpr"` overrides selected sources of the base project; `extends all` extends the whole import closure.
- `Library_Interface` (unit names) or `Interfaces` (source files) makes a stand-alone library; only the interface units may be imported from outside.
- `relocatable` is a synonym for `dynamic`.
- `Library_Kind` defaults to static. To build both static and dynamic variants use separate object directories.
## Gotchas
- The docs show `Library_Dir` different from `Object_Dir`; keep them apart.
- A project may not import both an extending project and a project it extends.
## Self-check
Build the library, then build a main whose project imports it.

## Checked
2026-11-03. Confirmed in the GPRbuild User's Guide (GNAT Project Manager chapter): `Library_Name`, `Library_Dir`, `Library_Kind` values, `Library_Interface`/`Interfaces`, `extends`, `extends all`, aggregate `Project_Files`. Removed the ldd/nm check and the unqualified rule that the two dirs must differ (the page only shows them different).
Method: documentation only; no commands were run.

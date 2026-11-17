---
id: computing-software.software-engineering.crystal.tool-hierarchy
name: tool-hierarchy
category: computing-software
field: software-engineering
product: crystal
tags: [tool-hierarchy, cli-tools, crystal-tool, class-hierarchy, ivar-sizes, memory-size, crystal]
level: advanced
status: docs-checked
description: "Use crystal tool hierarchy to print the type hierarchy with sizes, filter types by regex with -e, and get JSON output with -f json."
sources:
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/command.cr
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/tools/print_hierarchy.cr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crystal tool hierarchy

Goal: see the type tree and its memory cost.

- `crystal tool hierarchy src/app.cr` shows the type hierarchy of the program. The printer reports each type's kind (class, struct or union), its size and its instance variables with their sizes, when sizes are constant.
- Filter with `-e NAME`, a regex matched against type names (`-e Foo`); matching types and their related types and subtypes are printed.
- `-f text|json` / `--format text|json` selects the output; the default is `text`.
- Use it to spot a struct whose size makes copies costly, or an unexpectedly nilable instance variable (a union adds bytes).

Gotchas:
- Types whose instance variable types are not yet known have no size.
- The tool runs only the top-level semantic pass, not code generation.

Verify: the output includes your class with its instance variables.

## Checked

2026-11-03. Confirmed against the compiler source: tool list and `-e NAME` option (`command.cr`), format choices `text|json` and the size, kind and instance-variable output (`tools/print_hierarchy.cr`).
Removed: "compile errors prevent output", "generic instances appear separately per type argument" as a gotcha, and "sizes are for the compile target architecture", none of which the pages state.
Method: documentation only; no commands were run.

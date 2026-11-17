---
id: computing-software.software-engineering.crystal.tool-implementations-unreachable
name: tool-implementations-unreachable
category: computing-software
field: software-engineering
product: crystal
tags: [tool-implementations-unreachable, cli-tools, tool-implementations, tool-unreachable, tool-dependencies, tool-expand, dead-code, macro-expansion, tool-types, crystal]
level: advanced
status: docs-checked
description: "Use crystal tool implementations, unreachable, dependencies, expand, flags and types: cursor option, output formats, --tallies, --check, include and exclude."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/man/crystal/README.md
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/command.cr
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/tools/unreachable.cr
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/tools/dependencies.cr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tool implementations, unreachable, dependencies, expand, flags

Goal: use the other `crystal tool` subcommands.

- `crystal tool implementations -c f.cr:L:C f.cr` shows implementations for the call at the cursor (go to definition).
- `crystal tool expand -c f.cr:L:C f.cr` shows the macro expansion at the cursor.
- `crystal tool unreachable src/app.cr` lists methods that are never called. Formats: `-f text|json|csv|codecov` (the manual lists text, json and csv; the source also accepts codecov). `--tallies` also prints reachable methods with call counts; `--check` exits with error if any unreachable code exists; `-i PATH` / `-e PATH` include or exclude paths (exclude default: `lib`). Text columns: count (with `--tallies`), location, name, lines, annotations.
- `crystal tool dependencies src/app.cr` shows the tree of required files. `-f tree|flat|dot|mermaid` (default `tree`); `-i` / `-e` include or exclude paths; `--verbose` shows skipped and filtered paths.
- `crystal tool types` shows types of main variables; `crystal tool flags` prints all macro `flag?` values.
- `crystal tool` with no tool name prints the list (context, dependencies, expand, flags, format, hierarchy, implementations, macro_code_coverage, types, unreachable).

Gotchas:
- `unreachable` analyses the program reached from the entry file, so library API not used by the app appears unreachable.
- Cursor tools need `-c`/`--cursor LOC` (`path:line:column`); without it they print usage.

Verify: `crystal tool` lists subcommands matching these names.

## Checked

2026-11-03. Confirmed against the Crystal compiler manual (`tool` list, `dependencies` and `unreachable` options and text columns) and compiler source (`command.cr` tool dispatch and options, `command/cursor.cr`, `tools/unreachable.cr` formats, `tools/dependencies.cr` `Format` enum).
Fixed: removed "(confirm)" hedges by checking them; `dependencies` formats and `unreachable` formats are now stated from the source. Removed: "subcommand set varies by version".
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.crystal.tool-context
name: tool-context
category: computing-software
field: software-engineering
product: crystal
tags: [tool-context, cli-tools, cursor, local-types, editor-integration, inferred-types, crystal]
level: practitioner
status: docs-checked
description: "Use crystal tool context with -c file:line:col to list the typed local variables at a cursor position, with text or JSON output."
sources:
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/command.cr
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/command/cursor.cr
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/tools/context.cr
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/man/crystal/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crystal tool context

Goal: ask the compiler what a variable's type is at a spot.

- `crystal tool context -c src/app.cr:LINE:COL src/app.cr` shows the context (local variables and their types) at the given location. `-c LOC` / `--cursor LOC` takes `path/to/file.cr:line:column`; running without a cursor prints the usage.
- `-f json` / `--format json` gives JSON for editors; the default format is `text`.
- Use it when a union type is surprising: put the cursor after the assignment and read the type.
- Related tools sharing the cursor option: `crystal tool implementations -c file:L:C file` (implementations of the call at that location) and `crystal tool expand`. `crystal tool types` shows types of main variables. `crystal tool --help` lists the tools.

Gotchas:
- A method that is never called has no context; the tool reports "no context information found (methods which are never called don't have a context)".
- The tool compiles without code generation, so the program must type-check.

Verify: output lists the variable you pointed at with its inferred type.

## Checked

2026-11-03. Confirmed against the compiler source (`Command` tool list and option parsing, `cursor.cr`, `tools/context.cr` messages) and the Crystal compiler manual tool list.
Removed: "line and column are 1-based", the exact sample output `x : Int32 | String`, and the claim that code is analysed only if reachable from the entry file's requires.
Method: documentation only; no commands were run.

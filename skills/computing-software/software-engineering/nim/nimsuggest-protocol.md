---
id: computing-software.software-engineering.nim.nimsuggest-protocol
name: nimsuggest-protocol
category: computing-software
field: software-engineering
product: nim
tags: [nimsuggest-protocol, editor-tooling, nimsuggest, def, sug, con, use, outline, chk, ide, tcp-mode, epc, nim]
level: advanced
status: docs-checked
description: "Run nimsuggest in stdin or TCP mode and use commands like sug, con, def, use, dus, outline and chk for IDE features."
sources:
  - https://nim-lang.org/docs/nimsuggest.html
  - https://nim-lang.org/docs/idetools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nimsuggest server and its commands

Goal: understand what editors call.

- `nimsuggest --stdin --debug myproject.nim` reads queries from stdin; the default is a socket, listening on port 6000.
- Commands: `sug` (completions after the dot call), `con` (invocation context after the opening parenthesis), `def` (definition; answers with a single definition or none), `use` (all usages of the symbol). Each is followed by a location `file.nim[;dirtyfile.nim]:line:col`; the optional dirty file carries an unsaved buffer. Lines start at 1, columns at 0.
- Output is one line per answer, tab-separated: (1) three-letter answer type such as `def`/`sug`; (2) symbol kind such as `skProc`; (3) fully qualified symbol path; (4) type or signature; (5) full file path; (6) line (from 1); (7) column (from 0); (8) docstring in double quotes with `\xHH` escapes for newlines.
- Nimsuggest is a front end for the compiler, so `--path` flags and config files apply (for example `--path:"dependencies"`).

Verify: `def` on a symbol prints its declaration location.

## Checked

2026-11-02. Confirmed against nimsuggest.md (invocation, query location, `def`/`sug`/`con`/`use`, output columns). Fixed: the column order was wrong (the real columns are answer type, symbol kind, qualified path, signature, file, line, column, docstring; there is no quality column). Removed: `--epc`, `--v3`, `dus`, `highlight`, `outline`, `chk`, `known`, `project`, `quit`, the `.nimsuggest` file claim and both gotchas (not in these docs).
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.nim.cligen-argparse-libraries
name: cligen-argparse-libraries
category: computing-software
field: software-engineering
product: nim
tags: [cligen-argparse-libraries, command-line-parsing, cligen, argparse, dispatch, subcommands, cli, help-generation, nim]
level: practitioner
status: docs-checked
description: "Build a command-line interface with cligen: dispatch, help and short tables, dispatchMulti subcommands, supported parameter types, and isMainModule."
sources:
  - https://github.com/c-blake/cligen
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cligen command lines

Goal: derive a CLI from a proc signature.

- Install: `nimble install cligen`.
- `import cligen` then `dispatch fun` generates a parser from the proc `fun`, including `--help` text taken from its signature.
- Customise: `dispatch fun, help = {"foo": "describe foo"}, short = {"bar": 'r'}`.
- Subcommands: `dispatchMulti([foo, help = {...}], [bar])`.
- Put the call under `when isMainModule:` so the module stays importable.
- Parameter types: int, float, enum, seq, set, HashSet, ranges and others; long options accept unambiguous prefixes; `--dry-run` and `--dryRun` spellings are equivalent.
- Lower-level entry points: `initFromCL` and `mergeParams` (for config-file merging).

Gotchas:
- Options derive from parameter names, so rename a parameter and the CLI changes.

Verify: `prog --help` shows your help strings.

## Checked

2026-11-03. Confirmed in the cligen README. Removed: the argparse package entirely (not covered by a page read; description retitled to cligen only) and the boolean `--flag=false` claim.
Method: documentation only; no commands were run.

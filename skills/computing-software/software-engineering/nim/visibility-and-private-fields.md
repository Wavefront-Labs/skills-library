---
id: computing-software.software-engineering.nim.visibility-and-private-fields
name: visibility-and-private-fields
category: computing-software
field: software-engineering
product: nim
tags: [visibility-and-private-fields, modules, visibility, encapsulation, public-api, export-marker, api-design, nim]
level: practitioner
status: docs-checked
description: "Control what a Nim module exposes with the export marker, re-export modules, and deprecate names."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Visibility rules and module design

Goal: keep module APIs small.

- Each module is its own file and enables information hiding and separate compilation. Only top-level symbols marked with an asterisk (`*`) are exported when another module imports it.
- The export marker applies to procs, operators, variables, constants, types and object fields: `proc exportedEcho*(s: string)`, `var exportedVar*: int`, `const exportedConst* = 78`, `ExportedType* = object` with `exportedField*: int`.
- When the exported symbol of an `export` statement is another module, all of its definitions are forwarded, and an `except` list can exclude some symbols; you specify only the module name.
- `{.deprecated.}` marks a symbol as deprecated, optionally with a message: `proc thing(x: bool) {.deprecated: "use thong instead".}`.
- Method call syntax `obj.name(args)` is the same as `name(obj, args)` for any first argument type.

Verify: an external test module can call the exported API but not unmarked helpers.

## Checked

2026-11-08. Read the Nim manual Export marker section, the deprecated pragma section and the export/import forwarding paragraph, and the tutorial Modules paragraph on the asterisk.

Removed as unconfirmed: the `mypkg/private/` convention, constructor-proc and `##` documentation advice, the template and generic expansion remarks, and the transitive re-export warning. Dropped the lib index source (not used).

Method: documentation only; no commands were run.

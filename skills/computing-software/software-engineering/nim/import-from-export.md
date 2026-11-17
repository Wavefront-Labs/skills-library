---
id: computing-software.software-engineering.nim.import-from-export
name: import-from-export
category: computing-software
field: software-engineering
product: nim
tags: [import-from-export, modules, import, export, from-import, include, visibility, module, asterisk, nim]
level: practitioner
status: docs-checked
description: "Use import with except/only forms, qualified access, export markers, re-export and include for text inclusion."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# import, from, export and include

Goal: structure code across modules.

- Each module is its own file with its own namespace; the module name must be a valid identifier (file `identifier.nim`). Only top-level symbols marked with an asterisk are exported: `proc exportedEcho*(s: string)`, `var v*: int`, `const c* = 78`, `type T* = object` with `field*: int`.
- `import mod` brings the exports; a list is allowed (`import std/[os, strutils]`) or one module with an `except` list: ``import std/strutils except `%`, toUpperAscii``. The except list is not checked against the module's exports. `import` is only allowed at top level.
- `from std/strutils import `%`` imports named symbols for use without qualification; full qualification (`strutils.replace`) still works. `from module import nil` enforces fully qualified access.
- Alias with `as` (`import std/strutils as su`): the original name is then inaccessible. Subdirectories: `import dir / [moduleA, moduleB]`, or a string literal when a path part is not an identifier (`import "gfx/3d/somemodule"`). The module name stays the last component.
- Pseudo directories: `std` refers to the standard library, `pkg` to a Nimble package (search path, ignoring standard library locations). Importing stdlib modules with `std/` is recommended but not enforced.
- Re-export: `export B.MyObject` forwards a symbol so clients need not import its dependency; `export baz` forwards a whole module (with an optional `except` list). Name only the module when exporting a module.
- `include fileA, fileB` merely includes file contents (unlike import), can split a large module, and may be used outside top level, for example inside a proc body.
- Recursive module dependencies are allowed but subtle; an import can carry the `cyclic` pragma (`import b {.cyclic.}`) to declare a cycle, and annotating both sides is good practice.
- Ambiguity when two imports export the same identifier is resolved by qualifying it as `module.identifier`.

Verify: importing a module and calling a symbol without `*` fails to compile, while the starred one works.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md from the Nim repository): Export marker, Modules, Cyclic imports (read to the start of the phases list in detail), Import, Include, Module names in imports, Collective imports, Pseudo import/include paths, From import, Export statement and Scope rules (module scope, start). Removed because not stated there: relative `./sibling` and `../up/mod` imports, the claim that unexported fields block constructors, and the circular import workarounds. tut1 and lib were not read and were dropped from sources.
Method: documentation only; no commands were run.

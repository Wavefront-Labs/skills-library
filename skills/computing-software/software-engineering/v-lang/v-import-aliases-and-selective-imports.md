---
id: computing-software.software-engineering.v-lang.v-import-aliases-and-selective-imports
name: v-import-aliases-and-selective-imports
category: computing-software
field: software-engineering
product: v-lang
tags: [v-import-aliases-and-selective-imports, modules-and-imports, import, import-as, selective-import, module-prefix, v-lang]
level: practitioner
status: docs-checked
description: "Control names pulled in from modules: the default module prefix, selective imports of functions and types, and import aliases with as."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
  - https://docs.vlang.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Import aliases and selective imports

Goal: control the names a module brings into scope.

- Default: `import os` and call `os.input(...)`; you specify the module prefix every time you call an external function.
- A function declared in the current module, or held in a local variable, keeps its own behaviour even if it has the
  same name as a library function: `join_path('a', 'b')` calls the local binding, `os.join_path('a', 'b')` the `os` one.
- Selective import: `import os { input }`, or several: `import os { input, user_os }`. It imports specific functions and
  types. The docs note that this also imports the module, and that selective import is not allowed for constants:
  they must always be prefixed.
- Alias a module with `as`: `import mymod.sha256 as mysha256` lets it coexist with `import crypto.sha256`.
- Only public definitions of the module are available.
- A module path is determined by directories, not file names. With a hierarchy `abc/def`, `import abc.def` is needed
  to reach `def`, and its symbols use a single prefix (`def.func()`, not `abc.def.func()`), whatever the depth. Two
  modules with the same name in different directories need an alias.
- A module cannot import its own full path. Cyclic imports are not allowed.
- You cannot alias an imported function or type (you can redeclare a type).
- A module `init` function (not public) is called automatically, just once, however many times the module is imported.

Verify: import two modules that both end in `sha256`, alias one, and call both.

## Checked

Read the Module imports (selective imports, hierarchy, aliasing), `init` functions and Create modules sections of the V documentation (doc/docs.md from the vlang/v repository, the source of docs.vlang.io). Corrected: the draft said a selective import does not bind the module name, but the docs say it imports the module as well. Removed claims the page does not state: "run in import order", "cannot alias to a local variable's name", and "selecting a non-pub symbol is an error" (the docs only say public definitions are usable). Tags previously contained spaces and were fixed.

Method: docs-only read of cited pages, 2026-11-08

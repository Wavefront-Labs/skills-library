---
id: computing-software.software-engineering.v-lang.v-module-init-and-project-layout
name: v-module-init-and-project-layout
category: computing-software
field: software-engineering
product: v-lang
tags: [v-module-init-and-project-layout, modules-and-imports, init-function, cleanup-function, v-mod, module-lookup, project-layout, v-lang]
level: practitioner
status: docs-checked
description: "Use module init and cleanup functions, and lay out modules under the v.mod lookup root, including .v.mod.stop and the top-level folder exception."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
  - https://docs.vlang.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module init functions and project layout

Goal: organise a multi-module codebase.

- `fn init() { ... }` in a module is called automatically, just once, however many times the module is imported.
  It cannot be public. Useful for initialising a C library.
- `fn cleanup() { ... }` is called automatically when the program ends, once per module, in the reverse order of
  the `init` calls. It cannot be public either.
- Each module is a directory; its files start with `module name_of_folder`. Names should be short (under 10 characters)
  and `snake_case`; circular imports are not allowed; all modules compile statically into one executable.
- Only `pub` items are visible outside the module; items are shared between files of the module whether `pub` or not.
- The nearest `v.mod` is the lookup root: V prepends its folder to the module lookup path. A module's import path is
  its path under that root, e.g. `myapp/v.mod`, `myapp/main.v`, `myapp/mymod/`. There is no virtual `modules/` or `src/`
  root any more; move such directories up beside `v.mod`.
- An empty `.v.mod.stop` file in a root keeps lookup inside the project (upward search stops there). A `.git`, `.hg` or
  `.svn` entry stops selection of a parent's `v.mod` but not the upward module search.
- Only the top-level project folder compiled with `v .` may mix `module main`, `module abc`, etc. across its .v files.
  In ordinary modules every file must start with `module name_of_folder`.

Verify: put `fn init() { println('init') }` in a local module, import it from two files, and see it print once.

## Checked

Read the Modules (create modules, lookup root, aliases, special considerations for project folders, init and cleanup functions) sections of the V documentation (doc/docs.md from the vlang/v repository, the source of docs.vlang.io). Removed claims the page does not state: a recommended directory layout (`bin/`, `cmd/`, tests next to code), `$embed_file` shipping advice, global-state advice, "init order follows dependency order" and "init runs before main" wording. Tags previously contained spaces and were fixed.

Method: docs-only read of cited pages, 2026-11-08

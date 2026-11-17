---
id: computing-software.software-engineering.v-lang.v-module-declaration-and-import
name: v-module-declaration-and-import
category: computing-software
field: software-engineering
product: v-lang
tags: [v-module-declaration-and-import, modules-and-imports, module, import, pub, package, directory, namespace, v-lang]
level: intro
status: docs-checked
description: "Declare V modules per directory, import them with dotted paths, aliases and selective imports, export with pub, and know the circular import and naming rules."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declaring modules and importing

Goal: split code into modules.

- Every file in the root of a folder is part of the same module. Simple programs need no module name and default to `main`.
- Create a module with a directory containing `.v` files that start with `module name`. Items inside a module are usable across its files whether or not they are `pub`; export with `pub`.
- Module hierarchy: a module name in a file must match its directory name, and never repeats the hierarchy (`abc/def/source.v` starts with `module def`). Import with the full path (`import abc.def`) but refer to symbols with a single prefix (`def.func()`), so two same-named modules in different directories need `import mymod.sha256 as mysha256`.
- Selective imports: `import os { input, user_os }`. This imports the module too, and is not allowed for constants, which must be prefixed.
- Rules listed in the docs: module names short (under 10 characters) and `snake_case`; circular imports are not allowed; as many `.v` files as you like; modules can be anywhere under a valid lookup root; all modules compile statically into one executable.
- In normal projects the nearest `v.mod` is the lookup root and V prepends its folder to the module lookup path. An empty `.v.mod.stop` file keeps lookup inside a project.
- A module cannot import its own full path. You cannot alias an imported function or type, but you can redeclare a type (`type MyTime = time.Time`).
- A locally declared function keeps its own behaviour even if it shares a name with a library function; `os.join_path` still calls the library one.

Verify: `v .` from the project root builds, and calling a private function from outside the module fails.

## Checked
2026-11-08. Checked against the Modules and Imports sections of the V documentation (`doc/docs.md`). Removed (not stated): unused imports are errors, "file order does not matter", the claim that conditional platform file suffixes (`_windows.v`, `_nix.v`) are covered here, and the `mymod/mymod.v` layout. Replaced landing-page sources with the raw docs file.
Method: documentation only; no commands were run.

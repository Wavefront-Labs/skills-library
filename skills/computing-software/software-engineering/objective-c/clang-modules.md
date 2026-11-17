---
id: computing-software.software-engineering.objective-c.clang-modules
name: clang-modules
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-modules, clang-modules]
level: practitioner
status: docs-checked
description: "Enable modules with -fmodules, use @import and auto-linking, and understand the module map and umbrella header."
sources:
  - https://clang.llvm.org/docs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# Clang modules
**Goal:** import frameworks as modules for faster builds.

```objc
@import std;
@import std.io;
```
- Enable modules with `-fmodules`; that makes modules-enabled libraries available as modules and introduces module syntax.
- In Objective-C, `@import` imports the named module (`@import std;` the whole module, `@import std.io;` a submodule).
- `-fmodules-cache-path=<directory>` sets the module cache directory.
- `-fimplicit-module-maps` loads `module.modulemap` files without enabling modules, which only checks header usage; `-fmodule-map-file=` names a map file explicitly. `-fmodules` implies implicit module maps.
- A module map file describes which headers make up a module.

## Self-check
Compile a file with and without `-fmodules` and compare diagnostics.

## Checked
2026-11-02. Confirmed against the Clang "Modules" page: `-fmodules`, `@import` syntax, cache path flag, implicit module map options. Removed: Xcode build setting names, `CLANG_ENABLE_MODULES`/`CLANG_MODULES_AUTOLINK`, auto-linking, framework umbrella example, `-fcxx-modules`, macro-isolation and DerivedData remarks (not on the page).
Method: documentation only; no commands were run.

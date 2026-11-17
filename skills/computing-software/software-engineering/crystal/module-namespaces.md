---
id: computing-software.software-engineering.crystal.module-namespaces
name: module-namespaces
category: computing-software
field: software-engineering
product: crystal
tags: [module-namespaces, modules, namespace, nested-module, constant-lookup, require, top-level, double-colon, crystal]
level: practitioner
status: draft
description: "Organise code with nested modules and classes, resolve constants with ::, and use require paths to match."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Namespaces and nested modules

Goal: structure a library.

- `module Acme; class Client; end; end` defines `Acme::Client`; compact `class Acme::Client` works if `Acme` already exists.
- Constant lookup goes lexically outward, then the ancestors; `::Foo` forces top level.
- File layout convention: `src/acme.cr` requires `./acme/*`; `require "./foo/*"` loads all files in a dir (not recursive, alphabetical), `require "./foo/**"` is recursive.
- `require "json"` finds stdlib or `lib/` (shards); `require "./x"` is relative to the current file.

Gotchas:
- Cyclic requires are ignored after the first; order can matter for macros and inheritance.
- A shard named `foo-bar` is usually required as `foo-bar` (file name), check its `src` dir.
- Opening a stdlib class reopens it for the whole program (monkey patching), prefer your own module.

Verify: `crystal build` prints no undefined constant errors.

---
id: computing-software.software-engineering.erlang.module-attributes
name: module-attributes
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-modules, module-attributes]
level: intro
status: docs-checked
description: "Erlang module attributes: -module, -export, -export_type, -import, -vsn, -on_load, -compile and user-defined attributes."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module attributes and exports
**Goal:** lay out a module header correctly.

```erlang
-module(counter).
-export([start/0, inc/1]).
-export_type([t/0]).
-type t() :: pid().
-vsn("1.0").
-compile([{inline, [helper/1]}]).
-my_attr(value).                 % user attribute, readable via counter:module_info(attributes)
```
- `-module(Name)` is the only mandatory attribute, comes first, and the name must equal the file name minus `.erl` or code loading does not work as intended.
- Pre-defined attributes must be placed before any function declaration.
- `-compile(Options)` adds compiler options for this module (see the `compile` module). `-vsn(Vsn)` sets the version; the default is the MD5 of the module.
- User-defined attributes take one value and are returned by `Module:module_info(attributes)`; `module_info/0,1` also gives `module`, `compile`, `exports` and `md5`.
- `-import(Module, Functions)` lets you call functions without a module prefix; calling `lists:map/2` explicitly is clearer.

## Gotchas
- `-compile(export_all)` makes the compiler warn (suppress with `nowarn_export_all`); exporting everything also widens the public API.

## Self-check
Call `counter:module_info(exports)` and compare with your `-export` list.

## Checked
2026-11-02. Erlang Reference Manual "Modules" (pre-defined attributes, module_info, user attributes), Compiler `compile` docs (inline, export_all and its warning). Removed: flat namespace/prefix convention, xref and dead-code advice, "discouraged" wording on import, and the unused-function-warning claim for export_all.
Method: documentation only; no commands were run.

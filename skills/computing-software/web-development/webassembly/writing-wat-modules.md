---
id: computing-software.web-development.webassembly.writing-wat-modules
name: writing-wat-modules
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wat-module, wat2wasm, folded-instructions, wat, wasm-text-format, s-expressions, wasm]
level: practitioner
status: docs-checked
description: "Write WebAssembly text format (WAT) by hand and assemble it to .wasm with wat2wasm from wabt."
sources:
  - https://developer.mozilla.org/en-US/docs/WebAssembly/Guides/Understanding_the_text_format
  - https://developer.mozilla.org/en-US/docs/WebAssembly/Guides/Text_format_to_Wasm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing WAT by hand

Goal: write and assemble WAT.
- The text format is S-expression based; a module is one big S-expression, a tree of parenthesised nodes. Files use the `.wat` extension.
- Example: `(module (func $add (param i32 i32) (result i32) local.get 0 local.get 1 i32.add) (export "add" (func $add)))`. Parameters are read with `local.get` by numeric index (in declaration order) or by `$name`; Wasm is a stack machine, `i32.add` pops two `i32` values and pushes their sum, and the function result is the value left on the stack.
- Nested S-expression form is also accepted, as in `(global.set $g (i32.add (global.get $g) (i32.const 1)))`.
- Assemble with wabt: `wat2wasm add.wat -o add.wasm`; `wat2wasm add.wat -v` prints the binary layout; `wasm2wat add.wasm -o add.wat` converts back.
Verify: calling `add(2,3)` returns 5.

## Checked
Read the whole Text_format_to_Wasm page and the S-expressions, functions, locals, stack machine, exports and globals parts of Understanding_the_text_format (MDN) on 2026-11-08; the remaining sections (memory, tables, imports detail) were not read and the skill does not use them. Confirmed the S-expression model, `.wat` extension, `(param ...)`/`(result ...)`, `local.get` by index, `i32.add` stack behaviour, `(export "add" (func $add))`, nested instruction form, and the wat2wasm/wasm2wat commands and `-o`/`-v` flags. Removed: the term "folded form" (not used by MDN) and the "confirm" caveat.
Method: docs-only read of cited pages, 2026-11-08

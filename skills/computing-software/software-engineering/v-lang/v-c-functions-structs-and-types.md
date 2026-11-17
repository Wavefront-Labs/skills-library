---
id: computing-software.software-engineering.v-lang.v-c-functions-structs-and-types
name: v-c-functions-structs-and-types
category: computing-software
field: software-engineering
product: v-lang
tags: [v-c-functions-structs-and-types, c-interop, fn c, struct c, c namespace, typedef, extern, c enum, c function, v-lang]
level: advanced
status: docs-checked
description: "Redeclare external C functions with fn C.name and structs with struct C.Name, use @[typedef], opaque handles, variadics and C constants."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declaring C functions, structs and constants

Goal: call C from V.

- V cannot parse C headers, so redeclare what you use in `.c.v` files. A redeclaration needs only the parts you use, not the whole header.
- Functions: `fn C.name_of_the_C_function(param1 int, const_param2 &char, param3 f32) f64`. No body, name starts with `C.`, and capitals are allowed in the name. Prefix a `const char *` parameter with `const_` (needed for `-cstrict` and static analysers).
- Printf-style variadics use `...voidptr`, which ordinary V functions cannot: `fn C.dprintf(fd int, const_format &char, ...voidptr) int`.
- Structs: `struct C.NameOfTheStruct { a_field int }` can list only the fields you need. Structs created with `typedef struct SomeName {...} TypeName;` need `@[typedef]` and are named after the typedef: `@[typedef] pub struct C.TypeName {}`. The attribute is also needed for anonymous typedefs.
- Opaque handles: `pub struct C.sqlite3 {}` and use `&C.sqlite3`. C constants are read as `C.SQLITE_OK`; pointer constants such as `C.NULL` keep their pointer type.
- C globals: `@[c_extern] __global name C.Type` redeclares an external symbol (`__global const` for an `extern const`).
- Passing a V function by name to a `fn C.` callback parameter lets V adapt its parameter and return types to the C ABI.
- Interop types: `voidptr` is `void*`, `&u8` is `byte*`, `&char` is `char*`, `&&char` is `char**`. A C `int` array element is `i32`, since V's `int` storage is platform-width.

Gotchas:
- V does not check your redeclaration against the C header; a mismatch is a C compile or runtime error.
- Passing a C struct by value works as a return (`C.get_point(5).row`); on the experimental x64 native backend it is unsupported.

Verify: redeclare `fn C.dprintf` as above, call it with `c'...'` and check the printed text.

## Checked

2026-11-08. Read: the "V and C" sections of doc/docs.md (vlang/v) covering "Calling C from V" and "C types". Removed unconfirmed claims: `fn C.puts`/`C.sqrt`/`C.printf(fmt &char, ...)` signatures, `struct C.timeval` example, `const c_eof = C.EOF` advice, "no closures" for callbacks, "C functions are impure" gotcha and the claim that V `int` equals C `int`. docs.vlang.io and modules.vlang.io dropped from sources.
Method: documentation only; no commands were run.

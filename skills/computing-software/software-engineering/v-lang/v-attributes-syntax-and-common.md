---
id: computing-software.software-engineering.v-lang.v-attributes-syntax-and-common
name: v-attributes-syntax-and-common
category: computing-software
field: software-engineering
product: v-lang
tags: [v-attributes-syntax-and-common, attributes, inline, deprecated, export, packed, direct-array-access, noreturn, unsafe, heap, v-lang]
level: practitioner
status: docs-checked
description: "Apply V attributes to functions, structs, fields and enums: inline, unsafe, noreturn, heap, flag, required, noinit, must_use, export, with syntax rules."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attribute syntax and common attributes

Goal: use attributes correctly across versions.

- Syntax: an attribute is a compiler instruction in `@[...]` right before a function, struct or enum declaration; it applies only to the following declaration. Arguments work as `name: value` and call-style `name(value)` (call-style may use named arguments), for example `@[deprecated: 'use new_function() instead']` or `@[deprecated(msg: '...', after: '2021-05-27')]`.
- Several attributes on a field are separated by `;`, as in the docs `@[primary; serial]` and `@[deprecated: '...'; deprecated_after: '...']`.
- Functions (all in the docs): `@[inline]` (try to inline), `@[noinline]`, `@[unsafe]` (calls must be inside `unsafe {}`), `@[noreturn]` (no return type; ends in `for{}` or another noreturn call), `@[manualfree]`, `@[keep_args_alive]` (C interop), `@[must_use]` (ignoring the result warns), `@[deprecated]`, `@[export: 'c_name']`, `@[if flag ?]`, `@[live]`, `@[noalloc]`.
- Structs: `@[heap]` (must live behind a reference), `@[packed]`, `@[aligned]`, `@[minify]`, `@[noinit]` (cannot be initialised outside its module; provide a factory function), `@[typedef]` (C interop), `@[params]`.
- Fields: `@[required]` (must be initialised when creating the struct), `@[skip]` and `@[required]` for json decoding, `@[primary; serial]` for ORM ids, `@[deprecated: ...]`.
- Enums: `@[flag]` makes an enum usable as a bitfield; `@[_allow_multiple_values]` allows duplicate values.
- `@[direct_array_access]` translates array operations straight to C, omitting bounds checks. The docs say the tuning attributes are rarely needed: profile first.

Gotchas:
- The docs call `@[deprecated]` calls warnings, which become errors under `-prod`.
- `@[minify]` may break binary serialization or reflection.

Verify: call a function marked `@[deprecated]` and read the compiler diagnostic.

## Checked

Confirmed against the "Attributes", "Required fields", "[noinit] structs", "Performance tuning" and "Export to shared library" sections of doc/docs.md in the vlang/v repository, read 2026-11-08. Removed: the claim that old `[attr]` syntax is deprecated with a cutoff, `@[cold]`, `@[trusted]`, `@[markused]`, `@[autofree_bug]`, `@[omitempty]`, `@[has_globals]`, `@[json: ...]`/`@[sql: ...]` name forms (not located in the sections read), and the docs.vlang.io and modules.vlang.io sources.
Method: docs-only read of cited pages, 2026-11-08

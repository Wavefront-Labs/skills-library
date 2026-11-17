---
id: computing-software.software-engineering.v-lang.v-attributes-deprecated-export-and-codegen
name: v-attributes-deprecated-export-and-codegen
category: computing-software
field: software-engineering
product: v-lang
tags: [v-attributes-deprecated-export-and-codegen, attributes, deprecated, deprecated-after, export, direct-array-access, packed, minify, noinit, v-lang]
level: advanced
status: docs-checked
description: "Deprecate V functions with messages and dates, export C symbol names, and use inline, direct_array_access, packed, minify and noinit attributes."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deprecation, export and codegen attributes in practice

Goal: manage API evolution and performance.

- Deprecate with `@[deprecated]`, `@[deprecated: 'use new_function() instead']`, or a date: `@[deprecated: '...']` plus `@[deprecated_after: '2021-05-27']` (call-style: `@[deprecated(msg: '...', after: '2021-05-27')]`).
- Documented timeline with a date: before the date, calls are compiler notices; after it, calls are warnings (ordinary compiling still works, `-prod` fails because warnings are errors there); 6 months after the date, calls are hard compiler errors.
- Deprecation with no date is for functions found conceptually broken; otherwise the docs advise a date. To avoid breaking CI, set a future date; a date in the next 30 days assumes people compile manually at least once in that time.
- Struct field deprecations only notify on direct accesses from other modules.
- Export: `@[export: 'my_custom_c_name']` changes the C name (default is `[module name]__[fn_name]`, e.g. `bar__foo`); the same attribute exposes a `__global` from a shared library.
- Performance attributes (rarely needed; profile first): `@[inline]` costs executable size; `@[direct_array_access]` omits bounds checks (unsafe unless you check bounds); `@[packed]` costs speed for memory; `@[minify]` reorders struct fields to minimise gaps and may break binary serialization or reflection.
- `@[noinit]` structs cannot be initialised outside their module, only through factory functions such as `new_information(data) !Information`.
- Conditional compile: `@[if trace_logs ?]` on a function means it and its calls are not compiled unless `-d trace_logs` is passed; V still type checks them.

Gotchas:
- `direct_array_access` hides out-of-bounds bugs.
- Removing deprecated items breaks dependants; set a grace period.

Verify: compile a caller of a deprecated function and read the diagnostic.

## Checked

Confirmed against the "Attributes", "Conditional compilation", "[noinit] structs", "Performance tuning" and "Export to shared library" sections of doc/docs.md in the vlang/v repository, read 2026-11-08. Removed: the `-shared` pairing claim and the benchmark-under-`-prod` advice (not stated), and the docs.vlang.io and modules.vlang.io sources.
Method: docs-only read of cited pages, 2026-11-08

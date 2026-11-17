---
id: computing-software.software-engineering.d.d-ctfe-lookup-tables-and-parsers
name: d-ctfe-lookup-tables-and-parsers
category: computing-software
field: software-engineering
product: d
tags: [d-ctfe-lookup-tables-and-parsers, ctfe, ctfe-table, import-expression, string-import, compile-time-parser, embedded-resource, -j, d]
level: advanced
status: draft
description: "Compute tables, hashes and parsers at compile time, embed files with import(\"file\") and string imports, generate code from a DSL string."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Build lookup tables and parse DSLs with CTFE and import()

Goal: move work and data into the binary at compile time.

- Table: `static immutable ubyte[256] crcTable = makeTable();` where `makeTable` is `pure` and returns a static array; stored once in the data segment.
- Embed file: `enum data = import("template.txt");` requires `-Jdir` (dub `stringImportPaths "views"`). Content is `immutable(char)[]` (or cast to `ubyte[]` for binary).
- Parse at compile time: `enum cfg = parseConfig(import("cfg.ini"));` then use fields as constants.
- DSL to code: write a CTFE function turning a DSL string into D source, then `mixin(compile(dsl))` (vibe.d diet templates and pegged grammars do this).
- Regex at compile time: `ctRegex!"..."` (std.regex) builds a native matcher.
- Check results with `static assert` and run the same function at runtime in a unittest to compare.

Gotchas:
- `-J` paths are security-relevant: do not point at secrets.
- Large `import()`ed files lengthen compile time and memory.

Verify: change the imported file and observe the rebuild change the constant.

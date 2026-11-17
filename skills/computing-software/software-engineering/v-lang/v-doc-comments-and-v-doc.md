---
id: computing-software.software-engineering.v-lang.v-doc-comments-and-v-doc
name: v-doc-comments-and-v-doc
category: computing-software
field: software-engineering
product: v-lang
tags: [v-doc-comments-and-v-doc, comments-and-doc-comments, doc-comments, v-doc, documentation, vdoc, v-lang]
level: practitioner
status: docs-checked
description: "Write V doc comments directly above declarations, starting with the symbol name, add a module overview after the module line, and generate docs with v doc."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Doc comments and v doc

Goal: produce useful generated documentation.

- vdoc generates documentation from docstrings in the source, similar to Go. Documentation for each function, type or const goes right before the declaration, and the comment must start with the name of the definition: `// clearall clears all bits in the array`.
- Longer explanations span several single-line comments directly above the declaration. By convention comments are in present tense.
- An overview of the module goes in the first comment right after the module's name.
- Generate documentation with `v doc`, for example `v doc net.http`. The ANSI and HTML formats highlight enum values, attributes, map types, compile-time keywords and string interpolation format specifiers.
- Multi-line comments are merged with spaces, except around an empty line, a horizontal rule line (at least three of `-`, `=`, `_`, `*`, `~`), a header line (`# `), a table line (starting and ending with `|`) and a list line (starting with `- `).
- `v doc` follows the `.v.mod.stop` project boundary when resolving a module name.

Verify: `v doc` on your module lists the symbol with its comment text.

## Checked
2026-11-08. Checked against the Writing Documentation section of the V documentation (`doc/docs.md`). Removed (not stated there): the `v doc -f html -o` and `-readme` flags, the claim that only `pub` symbols appear by default, that a blank line detaches a comment, that examples are not compiled, and that the module comment goes *before* the `module` line (the docs place it right after the module name). Replaced landing-page sources with the raw docs file.
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.v-lang.v-string-methods-and-builder
name: v-string-methods-and-builder
category: computing-software
field: software-engineering
product: v-lang
tags: [v-string-methods-and-builder, strings, strings.builder, split, trim, replace, contains, starts_with, to_upper, join, v-lang]
level: practitioner
status: docs-checked
description: "Split, join, trim, replace, find, case-convert and efficiently build strings using the string methods and strings.Builder."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String methods and strings.Builder

Goal: do everyday text work.

- Query: `s.contains('x')`, `s.starts_with`, `s.ends_with`, `s.index('x')` (option), `s.count('a')`.
- Transform: `s.to_upper()`, `s.to_lower()`, `s.trim_space()`, `s.trim('x')`, `s.replace('a','b')`, `s.capitalize()`.
- Split/join: `s.split(',')`, `s.fields()` (whitespace), `parts.join('-')`, `s.split_into_lines()`.
- Substring: `s[2..5]`, `s.substr(a, b)`, `s.all_after('=')`, `s.all_before_last('/')`.
- Builder: `import strings; mut sb := strings.new_builder(64); sb.write_string('a'); sb.writeln('b'); out := sb.str()` (after `str()` the builder is empty and can be reused).

Gotchas:
- `s.index()` returns an option; use `or { -1 }` or `if i := s.index('x') {}`.
- Methods return new strings; the original is unchanged.

Verify: `assert 'a,b'.split(',') == ['a', 'b']`.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: string methods contains, starts_with, ends_with, index (returns ?int), count, to_upper, to_lower, trim_space, trim, replace, capitalize, split, fields, join, split_into_lines, substr, all_after, all_before_last (vlib/builtin/string.v); string slicing `name[1..3]` (doc/docs.md); strings.new_builder, write_string, writeln, str (vlib/strings/builder.c.v).
Removed or corrected: `(confirm)` on the builder reset; documented now as emptied after str().
Method: documentation only; no commands were run.

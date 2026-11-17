---
id: computing-software.software-engineering.nim.identifiers-style-insensitivity
name: identifiers-style-insensitivity
category: computing-software
field: software-engineering
product: nim
tags: [identifiers-style-insensitivity, lexical-analysis, identifier, style-insensitive, naming, camelcase, backticks, keywords, nim]
level: intro
status: docs-checked
description: "Understand Nim's partial case insensitivity, underscore stripping and keyword escaping with backticks."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identifiers and style insensitivity

Goal: name things so Nim code is portable and readable.

- Two identifiers are equal if the first letters match case-sensitively and the rest match case-insensitively (ASCII range) after ignoring underscores. So `fooBar` and `foo_bar` are the same, but `Foo` and `foo` differ. The manual calls this partial case-insensitivity.
- Its stated benefits: programmers can use their preferred spelling style (humpStyle or snake_style) and libraries with different conventions stay compatible. The first-letter exception allows code like `var foo: Foo` to parse unambiguously.
- The rule also applies to keywords: `notin`, `notIn` and `not_in` are the same, and all-lowercase is the preferred way to write keywords.
- A keyword enclosed in backticks loses its keyword property and becomes an ordinary identifier.
- Historically Nim was fully style insensitive (no distinction even between `foo` and `Foo`).

Verify: a symbol declared as `fooBar` can be referenced as `foo_bar`, but `FooBar` is a different identifier.

## Checked

2026-11-08. Read the Nim manual Identifier equality section and the keyword-in-backticks paragraph.

Removed as unconfirmed on the manual: the camelCase/PascalCase convention and leading-underscore advice, the `--styleCheck` switch and its verification, and the `importc` and grep gotchas. Dropped the tutorial and lib index sources (not used).

Method: documentation only; no commands were run.

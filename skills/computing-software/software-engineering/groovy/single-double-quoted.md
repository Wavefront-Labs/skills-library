---
id: computing-software.software-engineering.groovy.single-double-quoted
name: single-double-quoted
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, single-double-quoted, groovy-strings]
level: intro
status: docs-checked
description: "Single-quoted strings are plain java.lang.String; double-quoted may be GString with interpolation; escape rules and character literals."
sources:
  - https://groovy-lang.org/syntax.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-syntax.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single and double quoted strings
- `'text'` is always a `String`, no interpolation.
- `"text ${expr}"` is a `GString` when it contains an interpolated expression; otherwise a `String`.
- Escapes: `\n \t \\ \' \" \uXXXX`. Single char as `Character`: `'a' as char` or `(char) 'a'`.
- `"""` and `'''` are the multiline forms (see triple-quoted-slashy).

## Gotchas
- `"it costs $5"` is an error: `$5` is not a valid interpolation; write `"\$5"` (escaped) or use a single-quoted string.
- A `GString` and a `String` have different hashCodes, so a Map lookup with the other type fails: convert with `.toString()`.

## Self-check
`assert "a${1}" instanceof GString` and `assert 'a1' == "a${1}".toString()`.

## Checked

2026-11-02. Confirmed against the Syntax chapter (single-quoted, double-quoted strings, escapes, characters, interpolation, GString hashCodes). Removed: nothing beyond wording fixes.

Method: documentation only; no commands were run.

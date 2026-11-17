---
id: computing-software.software-engineering.nim.indentation-and-comments
name: indentation-and-comments
category: computing-software
field: software-engineering
product: nim
tags: [indentation-and-comments, lexical-analysis, indentation, comments, doc-comment, whitespace, line-continuation, nim]
level: intro
status: docs-checked
description: "Apply Nim's significant-whitespace rules, indentation in expressions, comment forms and documentation comments."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Indentation, comments and doc comments

Goal: format code the parser accepts.

- Nim is indentation sensitive: control structures are recognized by indentation, which consists only of spaces; tabulators are not allowed.
- Expressions can contain indentation for readability. As a rule of thumb, indentation within expressions is allowed after operators, an open parenthesis and after commas.
- No indentation is needed for a single-assignment statement after a condition on the same line; indentation is needed for a nested `if` or when two statements follow the condition.
- `# line comment`; `##` starts a documentation comment, for example `var myVariable: int ## a documentation comment`. Documentation comments are tokens that belong to the syntax tree, so they are only allowed at certain places in the input file.
- `#[ ... ]#` is a multiline comment and can be nested; inside it there are no indentation restrictions.

Gotcha: a documentation comment in a place the grammar does not allow is a syntax error.

Verify: nested `#[ ... ]#` comments out a block that itself contains `#[ ]#`.

## Checked

2026-11-08. Read the Nim tutorial sections on the first program, Comments, and Statements and indentation, and the manual Indentation section.

Removed as unconfirmed: the two-space convention, `nim doc` rendering of `##` lines, the module-level doc comment claim, the `;` multi-statement note and the mixed-tabs error message. Dropped the lib index source (not used).

Method: documentation only; no commands were run.

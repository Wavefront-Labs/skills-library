---
id: computing-software.software-engineering.d.d-comments-and-ddoc
name: d-comments-and-ddoc
category: computing-software
field: software-engineering
product: d
tags: [d-comments-and-ddoc, lexical-structure, ddoc, comments, documentation, nesting-comment, -d, d]
level: intro
status: docs-checked
description: "Use //, /* */, nesting /+ +/ comments and Ddoc (///, /** */) with Params, Returns, Examples sections, documented unittests and -D."
sources:
  - https://dlang.org/spec/ddoc.html
  - https://dlang.org/spec/lex.html
  - https://dlang.org/dmd-linux.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comments and Ddoc documentation comments

Goal: comment code and generate HTML docs.

- `//` line, `/* */` block (no nesting), `/+ +/` nests, so it can comment out code that already has comments.
- Ddoc comments: `///`, `/** ... */` or `/++ ... +/` placed directly before a declaration.
- Sections include `Params:`, `Returns:`, `Throws:`, `See_Also:`, `Examples:`, `Authors:` and `Bugs:`; each `Params:` line starts with an identifier followed by `=`.
- Macros look like `$(B bold)` or `$(LINK2 url, text)` (`B` boldfaces its argument; `LINK2` makes a clickable link).
- A `///` comment above a `unittest` block becomes a documented example (documented unittests).
- Generate with `dmd -D mod.d`; `-Dddirectory` sets the output directory and `-Dffilename` the output file.

Gotchas:
- `/* */` cannot nest, so commenting code with `/* */` breaks if it contains one.

Verify: run `dmd -D mod.d` and open the HTML; check the Params section is rendered.

## Checked
Checked 2026-11-03 against the D spec Embedded Documentation page (comment forms, sections, macros, documented unit tests), the Lexical page (nesting comments) and the dmd command-line page (`-D`, `-Dd`, `-Df`). Removed: the `---` compile-check claim, the blank-line attachment remark, `-o-` and the `Example:` section name (the page lists `Examples:`).

Method: documentation only; no commands were run.

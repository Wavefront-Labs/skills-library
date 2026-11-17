---
id: computing-software.software-engineering.d.d-identifiers-keywords-literals
name: d-identifiers-keywords-literals
category: computing-software
field: software-engineering
product: d
tags: [d-identifiers-keywords-literals, lexical-structure, literals, keywords, identifiers, integer-literal, float-literal, __file__, __line__, d]
level: intro
status: docs-checked
description: "Know D identifier rules, reserved words, integer and float literal forms: underscores, 0b, 0x, suffixes L u f, hex floats, and special tokens __FILE__."
sources:
  - https://dlang.org/spec/lex.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identifiers, keywords and numeric literals

Goal: read and write D literals correctly.

- Identifiers start with a letter, `_` or a universal alpha and continue with letters, `_`, digits or universal alphas; identifiers starting with two underscores are reserved.
- Integer literals: `1_000_000`, `0xFF`, `0b1010`; C-style octal such as `0167` is not supported, use `std.conv.octal`, e.g. `octal!167`.
- Suffixes: one `L` or `u`/`U` or both (there is no lowercase `l`); an unsuffixed decimal literal is `int` if it fits, then `long`, then `ulong`.
- Floats: `1.5`, `1e3`, in decimal or hexadecimal form; with no suffix the type is `double`, `f` gives `float` and `L` gives `real`; the imaginary `i` suffixes are deprecated.
- `__FILE__`, `__LINE__`, `__MODULE__`, `__FUNCTION__` and `__PRETTY_FUNCTION__` are keywords; `__DATE__`, `__TIME__`, `__TIMESTAMP__`, `__VENDOR__` and `__VERSION__` are special tokens.
- `__EOF__` tells the scanner to ignore everything after it; a leading `#!` shebang line is allowed.

Gotchas:
- `auto x = 3_000_000_000;` is long, not int.

Verify: `pragma(msg, typeof(0xFFFF_FFFF));` prints the deduced type at compile time (`uint` per the spec table).

## Checked
Checked 2026-11-03 against the D spec Lexical page (identifiers, integer and floating literals, keywords, special tokens, shebang). Removed: the "default arguments report the call site" remark and the integer-division remark (not on that page).

Method: documentation only; no commands were run.

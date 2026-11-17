---
id: computing-software.software-engineering.d.d-string-and-char-literals
name: d-string-and-char-literals
category: computing-software
field: software-engineering
product: d
tags: [d-string-and-char-literals, lexical-structure, string-literal, raw-string, token-string, wysiwyg, dchar, wstring, q-string, d]
level: practitioner
status: draft
description: "Choose among D string literal forms: double-quoted, raw r-strings, backtick, hex, delimited q-strings, token strings q{}, and the c w d suffixes."
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

# String, character and token-string literals

Goal: pick the right literal form and char width.

- `"..."` with escapes (`\n`, `é`, `\x41`); `r"..."` and `` `...` `` are raw (no escapes), good for regex and paths.
- `x"48 65 6C"` hex string; `q"EOS ... EOS"` heredoc; `q"(...)"` delimited (nesting brackets).
- `q{ ... }` token string: content must lex as D tokens, ideal for `mixin(q{...})` code.
- Suffixes `c` (immutable(char)[], UTF-8, default), `w` (wstring, UTF-16), `d` (dstring, UTF-32): `"hi"w`.
- Adjacent literals concatenate at compile time: `"a" "b"` is not allowed; use `~`, which folds constants.
- Chars: `'a'` is char, `'a'w` wchar, `'a'd` dchar.
- `string` is `immutable(char)[]`; `.length` counts UTF-8 code units.

Gotchas:
- Indexing a string gives code units; iterate with `foreach (dchar c; s)` for code points.
- Literal `\0` embedded is legal; string literals are also null-terminated, so `s.ptr` works with C (confirm for non-literals: use `toStringz`).

Verify: `assert("é".length == 2 && "é"d.length == 1);`

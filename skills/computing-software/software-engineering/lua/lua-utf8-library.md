---
id: computing-software.software-engineering.lua.lua-utf8-library
name: lua-utf8-library
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-utf8, utf8-library]
level: practitioner
status: docs-checked
description: "Process UTF-8 text with the utf8 library and know what Lua string functions do to multibyte data."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# utf8.len, codepoint, char and iteration
- `utf8.len(s [, i [, j [, lax]]])` returns the character count, or fail plus the position of the first invalid byte; `utf8.char(0x1F600)`; `utf8.codepoint(s, 1, -1)` returns code points of characters starting between bytes i and j.
- `for p, c in utf8.codes(s) do` gives byte position and code point and raises an error on an invalid sequence; `utf8.offset(s, n)` returns the byte position where the n-th character starts (negative n counts from the end; fail if out of range).
- `utf8.charpattern` is the pattern `"[\0-\x7F\xC2-\xFD][\x80-\xBF]*"`, matching one UTF-8 byte sequence in a valid UTF-8 string.
- By default the decoding functions reject surrogates; an extra `lax` argument makes them more permissive.
- `#s` is the byte length of a string, not a character count.
Verify: `utf8.len("héllo")` is 5 while `#"héllo"` is 6.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: utf8.len, utf8.char, utf8.codepoint, utf8.codes, utf8.offset, utf8.charpattern, section 8.2 (surrogates), section 2.1 (strings are byte sequences). Removed: the claims about string.upper/lower and %a in the C locale, and the statement that Lua 5.1 and LuaJIT lack the library with named rocks (outside the 5.4 manual).
Method: documentation only; no commands were run.

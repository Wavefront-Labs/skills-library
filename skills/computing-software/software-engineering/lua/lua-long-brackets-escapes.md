---
id: computing-software.software-engineering.lua.lua-long-brackets-escapes
name: lua-long-brackets-escapes
category: computing-software
field: software-engineering
product: lua
tags: [lua, long-brackets-escapes]
level: practitioner
status: docs-checked
description: "Write Lua string literals: escape sequences (z, x, u{}), decimal escapes, and [==[ long brackets ]==] without escaping."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String literals
- Quotes allow `\n \t \\ \" \'`, `\xXX` (exactly two hex digits), `\ddd` (decimal, up to 3 digits), `\u{XXX}` (UTF-8, braces mandatory), and `\z` which skips the following whitespace including line breaks.
- Long brackets `[[...]]`, `[=[...]=]` take text raw (no escapes), drop a newline immediately after the opening bracket, and end at the first closing bracket of the same level, so pick a level of `=` that does not appear inside.
- A comment starting with `--` followed by an opening long bracket is a long comment, such as `--[[ ... ]]`, and runs to the matching closing bracket.
Verify: `#"\u{20AC}"` is 3 (UTF-8 bytes).

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 3.1 (escape sequences, long brackets, comments). Removed: the `---[[` toggle trick (not on the page).
Method: documentation only; no commands were run.

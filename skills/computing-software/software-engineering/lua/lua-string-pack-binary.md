---
id: computing-software.software-engineering.lua.lua-string-pack-binary
name: lua-string-pack-binary
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-integer-bitops, string-pack-binary]
level: advanced
status: docs-checked
description: "Serialise binary structures with string.pack and string.unpack formats and endianness."
sources: ["https://www.lua.org/manual/5.4/manual.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# string.pack, unpack and binary data
- `string.pack("<I2 z s4", 1, "name", "data")` packs little-endian uint16, zero-terminated string and a length-prefixed string.
- `string.unpack(fmt, s, pos)` returns the values followed by the index of the first unread byte.
- Format options include `<` `>` `=` endianness, `i[n]` `I[n]` sizes, `s[n]` length-prefixed strings and `![n]` alignment; see manual section 6.4.2 for the full list.
- Available in Lua 5.3 and later.
Verify: unpack(pack(x)) round-trips.

## Checked

Date: 2026-11-02. Confirmed on Lua 5.4 manual section 6.4 (string.pack, string.unpack return of next position, format options list heading). Removed as not confirmed: the single-letter size list, `z`/`f d n` meanings, and the lua-struct suggestion for 5.1.

Method: documentation only; no commands were run.

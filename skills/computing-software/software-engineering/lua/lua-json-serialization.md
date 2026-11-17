---
id: computing-software.software-engineering.lua.lua-json-serialization
name: lua-json-serialization
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-json-data, json-serialization]
level: practitioner
status: docs-checked
description: "Encode and decode JSON with lua-cjson or dkjson and serialise tables safely."
sources:
  - https://raw.githubusercontent.com/openresty/lua-cjson/master/manual.adoc
  - https://dkolf.de/dkjson-lua/
  - https://raw.githubusercontent.com/rxi/json.lua/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON libraries and table serialisation
- `local cjson = require("cjson"); cjson.encode({a = 1}); cjson.decode(s)`; pure-Lua alternatives are dkjson (can use LPeg to speed up decoding when available; `json.encode(tbl, { indent = true })` pretty-prints) and rxi/json.lua (works with Lua 5.1 to 5.3 and LuaJIT, compact output only).
- cjson encodes a table with only positive integer keys of type number as a JSON array and every other table as an object; object keys must be numbers or strings. It does not use metamethods when serialising.
- cjson errors by default on infinity/NaN, tables nested more than 1000 levels, and excessively sparse arrays (tunable with `cjson.encode_invalid_numbers`, `cjson.encode_max_depth`, `cjson.encode_sparse_array`). rxi/json.lua also raises an error for sparse arrays, mixed key types and invalid numbers.
- JSON null: cjson decodes it as a lightuserdata NULL pointer, compared with `cjson.null`. In rxi/json.lua, `null` inside an array or object becomes `nil` and is lost on decode. dkjson uses `json.null`.
- Number precision: `cjson.encode_number_precision(n)` with n from 1 to 14 sets significant digits (default 14).
- Never use `load` to parse serialised data from untrusted sources: it compiles and runs Lua code. Use a real parser.
- Config files: return a table from a Lua file only when the source is trusted.
Verify: round-trip arrays, nulls and unicode.

## Checked
2026-11-08. Confirmed in the lua-cjson manual (OpenResty fork on GitHub; read via targeted sections), the dkjson page (targeted searches only) and the rxi/json.lua README (read in full). Removed: the empty-table-as-object behaviour and `encode_empty_table_as_object` (not in the manual read), and the double-precision remark about large integers.
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.lua.lua-lua-dsl-config
name: lua-lua-dsl-config
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-config-dsl, lua-dsl-config]
level: advanced
status: docs-checked
description: "Design configuration as Lua tables or function-call DSLs and load them with load and a restricted environment."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table-based DSLs and config loading
- A table constructor syntax gives a natural DSL: `server { host = "x", port = 80 }` works because `f{fields}` is sugar for `f({fields})` and `f"str"` for `f('str')`.
- Load config with `load(text, "=config", "t", env)`: mode `"t"` accepts only text chunks, and `env` becomes the chunk's first upvalue (`_ENV`), so give it only the DSL functions; collect results in tables you control. `load` returns the function, or `fail` plus the error message on a syntax error.
- Validate types and ranges after loading and report the key path in errors.
- Keep configs data-only for untrusted sources: a Lua config file is code, and an `env` table limits what it can call but is not a hardened sandbox (the manual notes only that malformed binary chunks can crash the interpreter, which is why mode `"t"` matters).
Verify: a config with an unknown key produces a helpful error.

## Checked
2026-11-08. Confirmed in the Lua 5.4 Reference Manual: section 3.4.10 (call sugar) and `load` (mode and env parameters), via targeted reads. Removed: the claim that config scripts can loop forever (not stated in the manual).
Method: documentation only; no commands were run.

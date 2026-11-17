---
id: computing-software.software-engineering.lua.lua-version-differences
name: lua-version-differences
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-versions, version-differences]
level: advanced
status: docs-checked
description: "Know the main differences between 5.1, 5.2, 5.3, 5.4 and LuaJIT, and write code that runs on several."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lua 5.3 to 5.4 compatibility, and detecting the version
- `_VERSION` is a string holding the running version; in the 5.4 manual it is "Lua 5.4".
- Incompatibilities from 5.3 to 5.4 (manual section 8): string-to-number coercion moved from the core to string metamethods (arithmetic only, not bitwise; `"1" + "2"` is an integer); overflowing decimal integer literals are read as floats; `__lt` no longer emulates `__le`; the integer numerical for loop never wraps around; a goto label cannot be declared where a same-named label is visible; `print` no longer calls `tostring`, so use `__tostring`; `math.random` starts with a random seed and uses a different algorithm; utf8 decoding rejects surrogates by default; `collectgarbage` options "setpause"/"setstepmul" are deprecated in favour of "incremental"; `io.lines` returns four values.
- New in 5.4 per the manual: `<const>` and `<close>` local attributes, to-be-closed variables, `coroutine.close`, `warn`, generational GC (`collectgarbage("generational")`), xoshiro256** for `math.random`.
- `load(chunk, name, "t", env)` supplies an environment through the first upvalue.
- Test the Lua versions you support in CI.
Verify: run the test suite on each interpreter.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: _VERSION, section 8.1 and 8.2 (incompatibilities with 5.3), section 3.3.7 (attributes), warn, coroutine.close, collectgarbage, math.random, load. Removed: the per-version feature lists for 5.1, 5.2, 5.3 and LuaJIT, the portability idioms (`table.unpack or unpack`, `loadstring`, `setfenv`), the claims about `//`, `math.pow` and `math.ldexp`, since the manual describes only 5.4 and its differences from 5.3.
Method: documentation only; no commands were run.

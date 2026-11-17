---
id: computing-software.software-engineering.lua.lua-load-env-sandbox
name: lua-load-env-sandbox
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-load-sandbox, load-env-sandbox]
level: advanced
status: docs-checked
description: "Run untrusted or configuration code with load and a restricted _ENV, and know the limits of Lua sandboxes."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# load, loadfile and restricted environments
- `load(chunk, chunkname, mode, env)`: `mode` is `"b"`, `"t"` or `"bt"` (default `"bt"`); pass `"t"` to accept text only. If the loaded function has any upvalues, its first upvalue (the `_ENV` of a main chunk) is set to `env`. `loadfile` takes a file name, `mode` and `env`.
- Loading malformed binary chunks signals an error, but Lua does not check the consistency of the code inside binary chunks, so running maliciously crafted bytecode can crash the interpreter. Never load untrusted binary chunks.
- On failure `load` returns fail plus the message instead of raising.
- Build a whitelist environment (`{print = print, math = math}`) that omits `os`, `io`, `require`, `debug`, `load`, `dofile`, `loadfile`; `package.loadlib` is documented as inherently insecure, so keep `package` out too.
- Strings share one metatable, so any string value reaches the `string` library methods; the environment table alone does not remove them.
- `debug.sethook` with a count hook can be used to interrupt long-running code; the manual says nothing about memory limits.
Verify: attempt `os.execute` inside the sandbox and confirm it errors.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: load (mode, env, upvalue rules, binary chunk warning, fail return), loadfile, package.loadlib (insecure), section 2.4 (one shared metatable per non-table type), debug.sethook (count). Removed: the `setfenv` note for 5.1, the claim that `string.dump` chunks 'can crash' beyond the manual wording, the `getmetatable` whitelist advice and the `rep(1e9)` example.
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.lua.lua-lua-security-practices
name: lua-lua-security-practices
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-security, lua-security-practices]
level: practitioner
status: docs-checked
description: "Avoid command injection with os.execute and io.popen, unsafe load of untrusted data and weak randomness."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Injection, unsafe load and command execution
- `os.execute` and `io.popen` pass the command to a shell/system; never concatenate user input into them. Validate against a whitelist or avoid the shell.
- `load`, `loadfile` and `dofile` on untrusted text execute code; `load` and `loadfile` take mode `"t"` to refuse binary chunks and an `env` argument to restrict globals. Running maliciously crafted bytecode can crash the interpreter.
- `package.loadlib` is documented as inherently insecure: it lets Lua call any function in any readable dynamic library.
- The default random generator is a pseudo-random generator (xoshiro256**) and is not documented as secure; use the OS random source or a vetted library for tokens.
- Keep C modules updated; memory-unsafe bugs in native modules affect the whole process.
Verify: test input containing shell metacharacters and long strings.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: os.execute, io.popen, load (mode, env, bytecode warning), loadfile, dofile, package.loadlib, math.random. Removed: the claim about exponential-time Lua patterns (the pattern section was not checked in this batch), `loadstring`, and the unsourced advice on reading OS random sources.
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.lua.lua-lua-cli-scripts
name: lua-lua-cli-scripts
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-standalone, lua-cli-scripts]
level: intro
status: docs-checked
description: "Run scripts with the lua command, read arguments from arg, set exit codes and use the REPL."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lua command, arg, shebang and exit codes
- `lua script.lua a b`; `arg[0]` is the script, `arg[1]..` are the arguments and arguments before the script name (interpreter and options) go to negative indices; the script is also called with `arg[1], ..., arg[#arg]` as its `...` arguments.
- Options: `-e stat` runs a string, `-i` enters interactive mode after running the script, `-l mod` requires `mod` and assigns it to the global `mod` (`-l g=mod` assigns to `g`, since 5.4.4), `-` runs stdin as a file and stops option handling, `--` stops option handling, `-v` prints the version, `-E` ignores environment variables, `-W` turns warnings on. `-e`, `-l` and `-W` are handled in the order they appear.
- Without a script, `lua` acts as `lua -v -i` when stdin is a terminal and as `lua -` otherwise. With no script, `arg[0]` is the interpreter name.
- A first line starting with `#` is skipped, so `#!/usr/bin/env lua` works after `chmod +x`.
- Exit codes: `os.exit(code [, close])`: `true` gives EXIT_SUCCESS, `false` gives EXIT_FAILURE, a number gives that status; the default is `true`. An unprotected error is reported to stderr with a stack traceback (a non-string error object with `__tostring` uses that for the message).
- Environment variables: `LUA_INIT_5_4` (or `LUA_INIT`; a value of the form `@filename` runs the file, otherwise it runs the string), `LUA_PATH_5_4` / `LUA_PATH` and `LUA_CPATH_5_4` / `LUA_CPATH`.
Verify: a script containing `print(#arg)` run as `lua script.lua a b` prints 2.

## Checked
2026-11-08. Confirmed in the Lua 5.4 Reference Manual section 7 (stand-alone interpreter, read in full), `os.exit`, and the `package` library for LUA_PATH and LUA_CPATH names. Removed: the claim that `-l mod` merely preloads, and the claim that an uncaught error returns exit code 1 (the manual does not state the status).
Method: documentation only; no commands were run.

---
id: computing-software.networking-hardware-and-wireless.asterisk.lua-dialplan-pbx-lua
name: lua-dialplan-pbx-lua
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, lua, pbx-lua, extensions-lua, dialplan, app-table, channel-table]
level: practitioner
status: docs-checked
description: "Write dialplan in Lua with pbx_lua: extensions.lua table of functions, the app and channel tables, get/set for variables and functions, reserved-word access, and reload."
sources:
  - https://docs.asterisk.org/Configuration/Dialplan/Lua-Dialplan-Configuration/
  - https://docs.asterisk.org/Configuration/Dialplan/Lua-Dialplan-Configuration/Dialplan-to-Lua-Reference/
  - https://docs.asterisk.org/Configuration/Dialplan/Lua-Dialplan-Configuration/Interacting-with-Asterisk-from-Lua-apps-variables-and-functions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lua dialplan (pbx_lua)
Build requirement: Lua development libraries must be installed before Asterisk is configured and built.

`extensions.lua` is a Lua script (not a standard Asterisk config file) that defines a global table `extensions`. Each extension is a function run when a channel lands there, called with the context and extension; there are no priorities. Pattern syntax matches `extensions.conf`, and includes are written `include = {"demo", "users"}`.
```lua
extensions = {
    default = {
        ["100"] = function(context, extension)
            app.playback("please-hold")
            app.dial("SIP/100", 60)
        end
    }
}
```
- Reload: `module reload pbx_lua`. On errors the old file stays in use; existing channels keep using it. Runtime errors are logged and the channel hung up.
- Applications: `app.name(args)`, names case-insensitive; use `nil` for skipped arguments.
- Variables: `channel.my_variable = "value"`; read with `channel.my_variable:get()` (plain `value = channel.my_variable` does not work).
- Functions: `channel.FAXOPT("modems"):set("v17,v27,v29")`.
- Names that are Lua reserved words need brackets: `app["goto"]("default", 1000, 1)` (`app.goto` fails to load with Lua 5.2 or later).
- Where macros or gosub were used, a Lua function usually suffices.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Lua-Dialplan-Configuration, Dialplan-to-Lua-Reference, Interacting-with-Asterisk-from-Lua-apps-variables-and-functions) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.

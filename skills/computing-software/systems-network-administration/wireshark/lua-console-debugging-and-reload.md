---
id: computing-software.systems-network-administration.wireshark.lua-console-debugging-and-reload
name: lua-console-debugging-and-reload
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, lua, lua-console, lua-debugging, dissector-development]
level: practitioner
status: verified
description: "Debug Wireshark Lua dissectors with the Lua console, print and logging calls, error tracebacks in the tree, and hot reload of Lua plugins."
sources:
  - https://www.wireshark.org/docs/wsdg_html_chunked/wsluarm.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChCustCommandLine.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging Lua with the console and reload

## Lua console
Tools > Lua Console (a single input/output dialog since 4.2, replacing the older Tools > Lua > Evaluate): run Lua
against the live Wireshark state, e.g. `print(Dissector.get("tcp"))` (prints `TCP`), `print(get_version())` (`4.4.1`),
`#DissectorTable.list()` (557 tables in 4.4.1).

## Reload without restarting
Analyze > Reload Lua Plugins (Ctrl+Shift+L; it is in the 4.4.1 binary and named in the 3.6.0 release notes) re-runs the
Lua scripts: edit, save, reload. Registering the same name twice is an error, so if reload complains after you rename
a protocol or field, restart (a second `Proto("name", ...)` with the same name raises
`there cannot be two protocols with the same name`; the name must also not collide with a built-in protocol).

## Seeing errors
- A runtime error in a dissector shows as `[Expert Info (Error/Undecoded): Lua Error: t1.lua:10: ...]` in the
  packet tree, with file, line and a `Lua Traceback`. Filter `_ws.expert.message contains "Lua Error"`.
- Load-time errors: tshark prints them to stderr (`tshark: Lua: syntax error:
  t4.lua:1: ...`, `tshark: Lua: Error during loading:`).

## Logging
```lua
print("len", buffer:len())               -- goes to the Lua console (GUI) or stdout (tshark)
report_failure("myproto: bad header")     -- error dialog in the GUI
```
The old `info()`, `debug()` and `critical()` logging globals are gone in 4.4.1: `info` is `nil`, `debug` is Lua's
standard debug library (a table) and `warn` is Lua 5.4's built-in (silent until enabled), so `info("x")` raises
`attempt to call a nil value (global 'info')`. Use `print`, and run tshark from a terminal to see it.

## Testing with tshark
```
tshark -X lua_script:myproto.lua -r sample.pcap -Y myproto -V
```
Fast feedback without the GUI; combine with a small sample file.

## Gotchas
- `tree:add` with a ProtoField type that does not fit the bytes fails only when a packet is dissected: an `ipv4` field
  given a 1-byte range printed `[Expert Info (Error/Malformed): Trying to fetch an IPv4 address with length 1]` and
  `[Malformed Packet: <proto>]`. Test with packets that exercise every branch.
- Global state survives between packets; reset per-file state in `proto.init`. In TShark 4.4.1 `init` ran twice for
  one file (at startup and when the file was opened), so make it idempotent.

## Verify
- [ ] After reload, the packet tree updates with no Lua Error expert items in the sample capture.

## Checked
Run with TShark 4.4.1 (Wireshark ships Lua 5.4, `lua54.dll`): a script using `print(get_version())`,
`Dissector.get("tcp")` and `DissectorTable.list()` ran; a Proto registered on tcp.port 8443 produced `Lua Error` expert
items when `info()` was called, and `_ws.expert.message contains "Lua Error"` matched them; type checks showed `info`,
`critical`, `message` nil, `debug` a table, `warn` and `report_failure` functions; syntax and load errors went to
stderr as quoted; duplicate Proto names raised the quoted error; `init` printed twice per run; a ProtoField/length mismatch produced the quoted Malformed expert item. `-X lua_script:` testing
runs as written. "Reload Lua Plugins" and its Ctrl+Shift+L shortcut found in the Wireshark.exe resources; the 4.2.0
release notes say the Lua console dialogs were merged into one window. GUI behaviour is as described in those sources.

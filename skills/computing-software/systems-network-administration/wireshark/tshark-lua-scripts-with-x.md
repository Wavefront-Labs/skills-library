---
id: computing-software.systems-network-administration.wireshark.tshark-lua-scripts-with-x
name: tshark-lua-scripts-with-x
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tshark-lua, lua, tshark, taps, automation]
level: practitioner
status: verified
description: "Run Lua scripts in tshark with -X lua_script and lua_script1 arguments: load dissectors, write taps that aggregate fields, and print reports per capture."
sources:
  - https://www.wireshark.org/docs/man-pages/tshark.html
  - https://www.wireshark.org/docs/wsdg_html_chunked/lua_module_Listener.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running Lua scripts with tshark -X

## Loading a dissector for one run
```
tshark -X lua_script:myproto.lua -r in.pcap -Y myproto
```
No need to install it in the plugins folder; useful in CI and on servers. A 10-line Proto registered on `udp.port` 5004 loaded this way matched
`-Y myproto` and `-e myproto.b0` returned the first payload byte (checked on TShark 4.4.1).

## Passing arguments
```
tshark -X lua_script:report.lua -X lua_script1:top=20 -r in.pcap -q
```
Per the man page `-X lua_scriptN:arg` passes the string to the Nth loaded script. Inside the script: `local args = {...}` gives `{"top=20"}` (checked: `#args` was 1 and `args[1]` was `top=20`).

## A tap that aggregates
```lua
local args = {...}
local top = tonumber((args[1] or ""):match("top=(%d+)")) or 10
local qname = Field.new("dns.qry.name")
local counts = {}
local tap = Listener.new("frame", "dns.flags.response == 0")
function tap.packet(pinfo, tvb)
  local q = qname()
  if q then local s = tostring(q); counts[s] = (counts[s] or 0) + 1 end
end
function tap.draw()
  local t = {}
  for k, v in pairs(counts) do t[#t+1] = {k, v} end
  table.sort(t, function(a, b) return a[2] > b[2] end)
  for i = 1, math.min(top, #t) do print(t[i][2], t[i][1]) end
end
```
Run with `-q` so per-packet lines are suppressed; `draw` runs at the end. This script, run on a test capture with one non-response DNS query, printed `1  xxxx...` (count, name).

## When to use Lua taps vs -T fields
- `-T fields | sort | uniq -c` is enough for simple counts.
- Lua taps keep state across packets (per-flow timers, request/response matching) in one pass.

## Gotchas
- `Field.new` must be called at script load, not inside `packet`: doing so fails with `A Field extractor must be defined before Taps or Dissectors get called`.
- Field extractors return nil when absent; multi-occurrence fields need `{f()}`: on a GRE packet with four `ip.addr` values `#{f()}` was 4 while `tostring(f())` showed only the first.

## Verify
- [ ] The report matches an equivalent `tshark -T fields ... | sort | uniq -c` on a sample.

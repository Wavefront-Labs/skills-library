---
id: computing-software.systems-network-administration.wireshark.lua-dissector-basics
name: lua-dissector-basics
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, wireshark-lua, lua-dissector, lua-dissector-proto, protofield, dissectortable, post-dissector, lua-tap, heuristic-dissector, plugins-folder, custom-protocol, reload-lua-plugins]
level: advanced
status: verified
description: "Write a Wireshark Lua dissector for a proprietary protocol: Proto and ProtoField, registering on a port, parsing a TvbRange, heuristics, post-dissectors and reloading plugins."
sources:
  - https://www.wireshark.org/docs/wsdg_html_chunked/wsluarm.html
  - https://www.wireshark.org/docs/wsdg_html_chunked/wslua_dissector_example.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lua dissector basics

## Minimal dissector
Example protocol on UDP 9999: 1-byte type, 2-byte length, payload.
```lua
local p = Proto("myproto", "My Protocol")
local f_type = ProtoField.uint8("myproto.type", "Type", base.DEC, {[1]="HELLO", [2]="DATA"})
local f_len  = ProtoField.uint16("myproto.len", "Length", base.DEC)
local f_data = ProtoField.bytes("myproto.data", "Data")
p.fields = { f_type, f_len, f_data }

local ef_short = ProtoExpert.new("myproto.short", "Truncated message", expert.group.MALFORMED, expert.severity.ERROR)
p.experts = { ef_short }

function p.dissector(tvb, pinfo, tree)
  if tvb:len() < 3 then return 0 end
  pinfo.cols.protocol = "MYPROTO"
  local sub = tree:add(p, tvb(), "My Protocol")
  sub:add(f_type, tvb(0,1))
  local len = tvb(1,2):uint()
  sub:add(f_len, tvb(1,2))
  if tvb:len() < 3 + len then sub:add_proto_expert_info(ef_short) return tvb:len() end
  sub:add(f_data, tvb(3,len))
  pinfo.cols.info = string.format("type=%d len=%d", tvb(0,1):uint(), len)
  return 3 + len
end

DissectorTable.get("udp.port"):add(9999, p)
```
Big-endian is default; use `:le_uint()` for little-endian fields (run: bytes 01 00 gave `uint()` 256 and `le_uint()` 1). Fields become filterable:
`myproto.type == 2`.

## Install and reload
- Put the file in the personal plugins folder (Help > About > Folders > "Personal Lua Plugins").
- Analyze > Reload Lua Plugins (Ctrl+Shift+L) after edits (menu item and shortcut found in the Wireshark 4.4.1 binary).
- Errors appear in the packet tree as Lua errors; Tools > Lua Console evaluates code (Ctrl+Return).
- tshark: `tshark -X lua_script:myproto.lua -r cap.pcapng -Y myproto` (run; output showed the HELLO/DATA names,
  the truncated-message expert info, and a 2-byte packet that returned 0 was left undissected).

## Over TCP
Messages span segments: use `dissect_tcp_pdus(tvb, tree, min_header_size, get_len_func, dissect_func)` so
Wireshark reassembles by your length field. `get_len_func(tvb, pinfo, offset)` returns the full PDU length and
`dissect_func(tvb, pinfo, tree)` handles one complete PDU (run: a 2-byte length protocol split over two TCP
segments was reassembled and both messages decoded, with the dissector registered for a TCP port range).

## Heuristic dissectors
For protocols on random ports: `p:register_heuristic("udp", function(tvb,pinfo,tree) if <magic
matches> then p.dissector(tvb,pinfo,tree) return true end return false end)`. Check a magic value
strictly to avoid false matches.

## Post-dissectors and taps
`register_postdissector(proto)` runs after all others for every packet: good for adding computed
fields (e.g. an "application latency" field from previous packets). `Listener.new("http")` taps
gather statistics across packets for custom reports (both ran: the post-dissector field appeared on every
packet and the tap's `packet`/`draw` callbacks fired once for the one HTTP request).

## Verify
- [ ] Sample capture decodes with correct field values; `myproto` filters work.
- [ ] Truncated packets show the expert info, not a Lua error.

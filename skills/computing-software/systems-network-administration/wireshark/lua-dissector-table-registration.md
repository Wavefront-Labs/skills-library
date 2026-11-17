---
id: computing-software.systems-network-administration.wireshark.lua-dissector-table-registration
name: lua-dissector-table-registration
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark-lua, dissector-table, lua-dissector, decode-as, heuristic, plugin-registration]
level: practitioner
status: verified
description: "Hook a Lua dissector into Wireshark properly: register in udp.port/tcp.port tables, add Decode As support, call sub-dissectors by table, and handle TCP reassembly."
sources:
  - https://www.wireshark.org/docs/wsdg_html_chunked/lua_module_Proto.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Registering Lua dissectors in dissector tables

A dissector does nothing until something hands it packets. Dissector tables map a key (UDP port,
ethertype, IP protocol, a parent protocol's type field) to a dissector.

## Register on a port
The protocol must already have its `dissector` function when you call `add`; otherwise Lua raises
"a Protocol that does not have a dissector cannot be added to a table" (seen in a run). Define fields and the
dissector first, register last.
```lua
local p_myproto = Proto("myproto", "My Protocol")
-- fields and dissector function defined here ...

local udp_table = DissectorTable.get("udp.port")
udp_table:add(5555, p_myproto)
DissectorTable.get("tcp.port"):add("7000-7002", p_myproto)
```
Find table names in Wireshark: View > Internals > Dissector Tables, or run `tshark -G dissector-tables`
(e.g. `ethertype`, `ip.proto`, `udp.port`, `tcp.port`).

## Allow Decode As instead of hard-coding
```lua
DissectorTable.get("udp.port"):add_for_decode_as(p_myproto)
```
Users then pick "MYPROTO" in Analyze > Decode As for any port, and the choice persists in the
profile's `decode_as_entries`.

## Your own sub-dissector table
If your protocol has a message-type field, let others (or later scripts) plug in per type:
```lua
local subtable = DissectorTable.new("myproto.type", "MyProto message type", ftypes.UINT8, base.DEC, p_myproto)
-- in the dissector:
local t = buf(0,1):uint()
local payload = buf(4):tvb()
if not subtable:try(t, payload, pinfo, tree) then
    Dissector.get("data"):call(payload, pinfo, tree)
end
```

## TCP: message boundaries
For TCP, one segment may carry part of a message or several messages:
```lua
function p_myproto.dissector(buf, pinfo, tree)
    local offset = 0
    while offset < buf:len() do
        if buf:len() - offset < 4 then
            pinfo.desegment_offset = offset
            pinfo.desegment_len = DESEGMENT_ONE_MORE_SEGMENT
            return
        end
        local msglen = buf(offset, 4):uint()
        if buf:len() - offset < msglen then
            pinfo.desegment_offset = offset
            pinfo.desegment_len = msglen - (buf:len() - offset)
            return
        end
        -- dissect one message at buf(offset, msglen)
        offset = offset + msglen
    end
end
```
Or use the `dissect_tcp_pdus` helper with a length function. The manual loop above was run against a
4-byte length-prefixed stream split across two segments: Wireshark showed `[2 Reassembled TCP Segments]` and
one tree item per message. Registering on a low port that another dissector already claims (the test hit the
IPA dissector on a source port 5000 conversation) can make the other dissector win on that packet; test with
high source ports.

## Verify
- [ ] Packets on the registered port show the protocol name, Decode As lists it, and messages split
  across segments decode once reassembled.

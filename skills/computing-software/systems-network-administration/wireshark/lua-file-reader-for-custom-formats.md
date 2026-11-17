---
id: computing-software.systems-network-administration.wireshark.lua-file-reader-for-custom-formats
name: lua-file-reader-for-custom-formats
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, lua, lua-file-reader, custom-file-format, wtap]
level: practitioner
status: verified
description: "Write a Wireshark Lua FileHandler to open proprietary log or capture formats as packets, with read, seek_read, open heuristics and encapsulation choice."
sources:
  - https://www.wireshark.org/docs/wsdg_html_chunked/lua_module_File.html
  - https://wiki.wireshark.org/Lua/Examples
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lua file readers

A Lua `FileHandler` teaches Wireshark (and tshark) to open a file format it does not know: device
logs with hex dumps, vendor trace formats, CSV of frames.

## Skeleton
```lua
local fh = FileHandler.new("Vendor hex log", "vendorhex", "Reads vendor hex logs", "rs")

local function parse_line(line)
  local ts, hex = line:match("^(%d+%.%d+)%s+([%x ]+)$")
  if not ts then return nil end
  return tonumber(ts), Struct.fromhex(hex:gsub(" ", ""))
end

fh.read_open = function(file, capture)
  local line = file:read("*l")
  if not line or not line:match("^VENDORLOG v1") then return false end
  capture.encap = wtap_encaps.ETHERNET
  capture.time_precision = wtap_tsprecs.USEC
  return true
end

local function read_common(file, frame)
  local line = file:read("*l")
  if not line then return false end
  local ts, data = parse_line(line)
  if not ts then return false end
  frame.time = NSTime(math.floor(ts), (ts % 1) * 1e9)
  frame.data = data
  frame.captured_length = #data
  frame.original_length = #data
  frame.flags = wtap_presence_flags.TS + wtap_presence_flags.CAP_LEN   -- without TS the time stays unset
  return true
end

fh.read = function(file, capture, frame)
  local pos = file:seek()
  if not read_common(file, frame) then return false end
  return pos                       -- offset used later by seek_read
end
fh.seek_read = function(file, capture, frame, offset)
  file:seek("set", offset)
  return read_common(file, frame)
end
register_filehandler(fh)
```

## Notes
- Run on Wireshark 4.4.1 with a 3-line vendor log: frames decoded as Ethernet/IP/UDP, `-2` (two-pass, which uses
  `seek_read`) worked, and `tshark -w` wrote a pcap. Without the `frame.flags` line the packets decoded but
  `frame.time_epoch` was empty (the timestamp was not applied). `wtap_presence_flags` names in 4.4.1 are `TS`,
  `CAP_LEN`, `INTERFACE_ID`, `SECTION_NUMBER`; print the table in your version before relying on a name.
- `read_open` must be cheap and strict: return false quickly for other formats, since Wireshark
  tries readers in turn.
- Choose `capture.encap` to match what the bytes are (ETHERNET, RAW_IP, USER0 for custom).
- Install in the personal Lua plugins folder (Help > About > Folders); reload with Ctrl+Shift+L.

## Verify
- [ ] `tshark -r vendor.log` lists frames with correct timestamps and decodes the payload protocol.

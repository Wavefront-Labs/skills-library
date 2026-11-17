---
id: computing-software.game-programming.multiplayer-networking.packet-capture-and-wireshark-dissectors
name: packet-capture-and-wireshark-dissectors
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, wireshark-dissector, packet-capture, debugging, game-programming]
level: practitioner
status: draft
description: "Debug game protocols with packet capture: tcpdump and Wireshark filters, writing a Lua dissector for a custom UDP protocol, and decrypting dev traffic."
sources: ["https://www.wireshark.org/docs/wsdg_html_chunked/wsluarm.html", "https://www.tcpdump.org/manpages/tcpdump.1.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Packet capture and Wireshark dissectors

**Goal:** see exactly what your game sends on the wire, decoded field by field.

## Capture
```bash
sudo tcpdump -i any -w game.pcap udp port 7777            # server side
tshark -i 1 -f "udp port 7777" -w game.pcapng             # Windows/Linux with tshark
```
Wireshark display filters: `udp.port == 7777 && frame.len > 1200` (near-MTU packets),
`udp.length < 20` (keepalives). Statistics -> Conversations/IO Graph gives packet rate and bandwidth.

## Lua dissector
```lua
local p = Proto("mygame", "MyGame Protocol")
local f_seq  = ProtoField.uint16("mygame.seq", "Sequence")
local f_ack  = ProtoField.uint16("mygame.ack", "Ack")
local f_type = ProtoField.uint8("mygame.type", "Type", base.DEC, {[1]="Input",[2]="Snapshot"})
p.fields = { f_seq, f_ack, f_type }
function p.dissector(buf, pinfo, tree)
  pinfo.cols.protocol = "MYGAME"
  local t = tree:add(p, buf(), "MyGame")
  t:add_le(f_seq, buf(0,2)); t:add_le(f_ack, buf(2,2)); t:add(f_type, buf(4,1))
end
DissectorTable.get("udp.port"):add(7777, p)
```
Put the file in Wireshark's personal plugins folder (Help -> About -> Folders). Use `add_le` for
little-endian fields. Bit-packed protocols need manual bit extraction with `buf:bitfield`.

## Encrypted traffic
Add a dev-build option to disable encryption or log session keys, and never ship it enabled.
Alternatively log decoded packets in-process alongside sequence numbers and correlate with captures.

## Uses
- Verify sizes match bandwidth budget and MTU limits.
- Find retransmission storms, duplicated sends, wrong ports after NAT.

## Verify
- Capture a session and confirm the dissector decodes every packet type with no malformed entries.

---
id: computing-software.systems-network-administration.wireshark.user-dlt-custom-link-types
name: user-dlt-custom-link-types
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, user-dlt, link-layer-type, dlt-user, custom-encapsulation]
level: practitioner
status: verified
description: "Map captures using DLT_USER0-15 to a dissector with the User DLTs table so proprietary or custom link-layer captures decode."
sources:
  - https://wiki.wireshark.org/HowToDissectAnything
  - https://www.wireshark.org/docs/wsug_html_chunked/ChUserDLTsSection.html
  - https://www.tcpdump.org/linktypes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User DLT table for custom link types

Link types 147-162 (`DLT_USER0`-`DLT_USER15`) are reserved for private use. Captures from custom
hardware, simulators or Lua-produced files often use them, and Wireshark shows only raw data.

## Configure
Edit > Preferences > Protocols > DLT_USER > Encapsulations Table > Edit:
| DLT | Payload protocol | Header size | Header protocol | Trailer size | Trailer protocol |
|-----|------------------|-------------|-----------------|--------------|------------------|
| User 0 (DLT=147) | eth_withoutfcs | 0 | | 0 | |
| User 1 (DLT=148) | ip | 4 | mycustomhdr | 2 | |

"Payload protocol" takes a registered dissector name (`eth_withoutfcs`, `eth_withfcs`, `ip`, `ipv6`, `udp`,
`sll_v1`/`sll_v2` (not `sll`), `wlan` or a Lua dissector name); an unknown name is rejected with "dissector not found".
The header and trailer protocol columns need dissector names too (`eth` is not one; use `eth_withoutfcs`). Header/trailer sizes skip vendor bytes before/after the payload.

The table is saved as `user_dlts` in the profile, so it travels with the profile; on the command line set a row with
`-o 'uat:user_dlts:"User 0 (DLT=147)","eth_withoutfcs","0","","0",""'`.

## Writing files with a user DLT
```
text2pcap -l 147 hex.txt out.pcap
editcap -T user0 in.pcap out.pcap          # relabel an existing file
```
Then decode with the table above. For a fully custom header, write a Lua dissector and register
it in the `wtap_encap` dissector table, or name it in the User DLT table.

## Verify
- [ ] Frames show the configured protocol tree, and header bytes are attributed to the header dissector or skipped.

## Checked (2026-10-22)
- Ran on Wireshark 4.4.1: `text2pcap -l 147 hex.txt out.pcap` produced a file with encapsulation `USER 0` that shows as raw data; with `-o 'uat:user_dlts:"User 0 (DLT=147)","eth_withoutfcs","0","","0",""'` the same file decoded as Ethernet/IP/UDP; payload `ip` with header size 14 and header protocol `eth_withoutfcs` also worked; payload `udp` with header 34 worked; `wlan` loaded but the frame was malformed (wrong protocol for the data); `sll`, header protocol `eth` and a made-up name failed with "dissector not found", while `sll_v1` and `sll_v2` load (names from `tshark -G dissectors`). `editcap -T user0 in.pcap out.pcap` relabelled an Ethernet file to `USER 0` (`editcap -T help` lists user0 to user15 ...).
- DLT_USER0-DLT_USER15 = link types 147-162, reserved for private use, from https://www.tcpdump.org/linktypes.html.
- `tshark -G protocols` lists the `DLT_USER` protocol (preferences name `user_dlt`) and `tshark -G dissector-tables` lists the `wtap_encap` table the skill mentions. Not run: the GUI dialog itself and Lua dissectors.

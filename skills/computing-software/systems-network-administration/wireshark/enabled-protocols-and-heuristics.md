---
id: computing-software.systems-network-administration.wireshark.enabled-protocols-and-heuristics
name: enabled-protocols-and-heuristics
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, enabled-protocols, heuristic-dissectors, dissector-tuning, decode-as]
level: practitioner
status: verified
description: "Disable misfiring dissectors and toggle heuristic dissectors in Wireshark Enabled Protocols, with tshark --disable-protocol and --enable-heuristic."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChCustProtocolDissectionSection.html
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enabled protocols and heuristic toggles

## The problem
Wireshark guesses protocols by port and by heuristics. Random high-port UDP decoded as "Skype" or
"RTP", or a proprietary protocol on 443 shown as broken TLS, misleads analysts.

## Enabled Protocols dialog
Analyze > Enabled Protocols (Ctrl+Shift+E):
- Untick a protocol to stop dissecting it entirely (payload shows as the parent's data).
- Heuristic sub-entries end in `_udp`, `_tcp` etc. (e.g. `rtp_udp`, `stun_udp`, `bt_utp_udp`, `skype_udp`; the name
  is the short name in `tshark -G heuristic-decodes`, not the protocol name): tick to enable guesswork, untick to stop
  false positives. Some are on by default (`stun_udp`), others off (`rtp_udp`, `skype_udp`).
- Search box filters the list. Saved per profile in `disabled_protos` (on by default, now off), `enabled_protos`
  (off by default, now on) and `heuristic_protos` (`name,1` or `name,0` per line).

## tshark
```
tshark -r in.pcapng --disable-protocol skype --disable-heuristic stun_udp
tshark -r voip.pcapng --enable-heuristic rtp_udp -Y rtp
tshark -G heuristic-decodes | grep -i rtp     # list heuristic names and default state
```
`-G heuristic-decodes` prints tab-separated columns: parent protocol, protocol, enabled now, enabled by default,
heuristic short name, description (e.g. `udp  rtp  F  F  rtp_udp  RTP over UDP`). `--disable-protocol` and
`--disable-heuristic` with an unknown name stop with `No such protocol <name>`.

## Decide what to use
- Port or address known: Decode As is precise.
- Ports dynamic (RTP without signalling in the capture): enable the heuristic.
- A dissector crashing or slowing analysis of huge files: disable it (e.g. disable `smb2`
  dissection when you only need TCP timing).

## Gotchas
- Disabling a protocol hides its children; with `--disable-protocol ip` the packet list shows only
  `Ethernet ... IPv4` and nothing above IP decodes. Disabling `tcp` leaves a `Data` blob under IP.
- Settings are per profile; capture what you changed in the analysis notes.

## Verify
- [ ] The false decode is gone and the expected protocol appears in Statistics > Protocol Hierarchy.

## Checked
Run with TShark 4.4.1: `--enable-heuristic rtp_udp` turned 0 RTP matches into 5 on a synthetic RTP-on-port-30002 pcap;
`-G heuristic-decodes` rows and defaults read directly (`stun_udp` T/T, `rtp_udp` F/F, `skype_udp` F/F,
`bt_utp_udp` F/F); `--disable-protocol skype --disable-heuristic stun_udp` accepted; unknown names rejected;
`--disable-protocol ip` and `--disable-protocol tcp` outputs observed. File names and the Shift+Ctrl+E shortcut from
the 4.4.1 manual pages and User's Guide shipped with the install.
